import os

from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.utils.html import format_html
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import (
    FORM_FIELD_CHOICES,
    AbstractEmailForm,
    AbstractFormField,
)
from wagtail.contrib.forms.views import SubmissionsListView
from wagtail.documents import get_document_model  # noqa
from wagtail.documents.models import Document
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtailcaptcha.forms import WagtailCaptchaFormBuilder
from wagtail.contrib.forms.forms import FormBuilder

from recruitment.views import send_email_job


class CustomSubmissionsListView(SubmissionsListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.is_export:
            # generate a list of field types, the first being the injected 'submission date'
            field_types = ["submission_date"] + [
                field.field_type for field in self.form_page.get_form_fields()
            ]
            data_rows = context["data_rows"]

            for data_row in data_rows:
                fields = data_row["fields"]

                for idx, (value, field_type) in enumerate(zip(fields, field_types)):
                    if field_type == "document" and value:
                        if value and (
                            value.startswith("http") or value.startswith("/")
                        ):
                            # Transform the plain text URL into a styled HTML button
                            fields[idx] = format_html(
                                '<a href="{}" target="_blank" class="button button-small button-secondary" '
                                'style="white-space: nowrap; background-color: #2e8da1; color: white;">'
                                "Voir le document</a>",
                                value,
                            )

        return context


class CustomFormBuilder(FormBuilder):
    def create_document_field(self, field, options):
        return forms.FileField(
            widget=forms.FileInput(
                attrs={
                    "accept": ".pdf, .doc, .docx",
                }
            ),
            **options,
        )


class ContractType(models.Model):
    page = ParentalKey(
        "recruitment.RecruitmentIndexPage",
        related_name="contract_types",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, verbose_name="Type de contrat")
    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name


class TestimonialCollaboratorBlock(blocks.StructBlock):
    name = blocks.CharBlock(label="Nom")
    role = blocks.CharBlock(label="Poste")
    quote = blocks.TextBlock(label="Citation")
    photo = ImageChooserBlock(label="Photo", required=False)

    class Meta:
        icon = "user"
        label = "Témoignage Collaborateur"


class JobApplicationFormField(AbstractFormField):
    field_type = models.CharField(
        verbose_name="field type",
        max_length=16,
        choices=list(FORM_FIELD_CHOICES) + [("document", "Upload Document")],
    )
    page = ParentalKey(
        "recruitment.RecruitmentIndexPage",
        related_name="form_fields",
        on_delete=models.CASCADE,
    )


class RecruitmentIndexPage(AbstractEmailForm):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )
    introduction = RichTextField(blank=True)

    testimonials = StreamField(
        [("testimonial", TestimonialCollaboratorBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Témoignages collaborateurs",
    )
    hide_on_pc = models.BooleanField(default=True, verbose_name="Masquer sur PC")

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        InlinePanel("contract_types", label="Types de contrat"),
        InlinePanel("form_fields", label="Application poste fixe"),
        # InlinePanel("spontaneous_application", label="candidate spontanée"),
        FieldPanel("testimonials"),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel("hide_on_pc"),
    ]

    subpage_types = ["RecruitmentPage"]
    form_builder = CustomFormBuilder
    submissions_list_view_class = CustomSubmissionsListView

    class Meta:
        verbose_name = "Page Recrutement"

    def get_context(self, request, *args, **kwargs):
        from home.models import CulturePage

        context = super().get_context(request, *args, **kwargs)

        jobs = RecruitmentPage.objects.live().public().order_by("-date")

        search = request.GET.get("search")
        if search:
            jobs = jobs.filter(
                Q(title__icontains=search)
                | Q(job_title__icontains=search)
                | Q(body__icontains=search)
            )

        paginator = Paginator(jobs, 6)
        page_number = request.GET.get("page")
        context["jobs"] = paginator.get_page(page_number)
        context["search_query"] = search

        ## culter page #####
        culture_page = CulturePage.objects.live().public().first()
        context["culture_page"] = culture_page if culture_page else []

        return context

    def serve(self, request):
        self.request = request
        if request.method == "POST":
            form = self.get_form(request.POST, request.FILES)
            if form.is_valid():
                self.process_form_submission(form)
                if request.htmx:
                    messages.success(request, "Message envoyé avec succès")
                    return render(
                        request,
                        "snippets/success.html",
                        {"page": self},
                    )
        return super().serve(request)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        for name, field in form.fields.items():
            # Only for inputs / textareas
            if hasattr(field.widget, "attrs"):
                field.widget.attrs.setdefault("placeholder", field.label)

        return form

    def process_form_submission(self, form):
        from contact.models import ContactPage

        cleaned_data = form.cleaned_data
        recruitment_page_id = self.request.POST.get("recruitment_page_id")
        if recruitment_page_id:
            try:
                recruitment_page = RecruitmentPage.objects.get(pk=recruitment_page_id)
                cleaned_data["recruitment_page"] = (
                    recruitment_page.title
                )  # Store title instead
            except RecruitmentPage.DoesNotExist:
                cleaned_data["recruitment_page"] = "Candidature Spontanée"

        for name, field in form.fields.items():
            if isinstance(field, forms.FileField):
                uploaded_file = cleaned_data.get(name)
                if uploaded_file:
                    document = Document.objects.create(
                        title=os.path.basename(uploaded_file.name),
                        file=uploaded_file,
                    )
                    # Store document ID or URL
                    cleaned_data[name] = self.request.build_absolute_uri(document.url)
                else:
                    cleaned_data[name] = ""

        data = {}
        for name, field in form.fields.items():
            value = cleaned_data.get(name)

            # If it's a file, store the URL instead of the file object
            if isinstance(field, forms.FileField) and value:
                data[name] = value.url if hasattr(value, "url") else value
            else:
                data[name] = value

        recipients_emails = ContactPage.objects.first().get_recipient_list()
        print("recipients_emails------------------------->>>", recipients_emails)
        if recipients_emails:
            send_email_job(
                self.request,
                recipients_emails,
                data={
                    "recruitment_page": cleaned_data["recruitment_page"],
                    "data": data,
                },
            )
        print("--------------------email sent----------------------------------")

        return super().process_form_submission(form)

    #### to display name of job with the form on admin
    def get_data_fields(self):
        data_fields = super().get_data_fields()
        data_fields.append(("recruitment_page", "Poste pourvu"))

        return data_fields

    # def get_submission_class(self):
    #     """
    #     We override the submission class behavior to format the file URLs as buttons
    #     """
    #     submission_class = super().get_submission_class()
    #     parent_page = self

    #     class CustomSubmission(submission_class):
    #         def get_data(self):
    #             data = super().get_data()

    #             # Identify which fields are 'document' types from the page definition
    #             document_fields = parent_page.form_fields.filter(field_type="document")
    #             doc_field_names = [f.clean_name for f in document_fields]

    #             for field_name in doc_field_names:
    #                 value = data.get(field_name)
    #                 if value and (value.startswith("http") or value.startswith("/")):
    #                     # Transform the plain text URL into a styled HTML button
    #                     data[field_name] = format_html(
    #                         '<a href="{}" target="_blank" class="button button-small button-secondary" '
    #                         'style="white-space: nowrap; background-color: #2e8da1; color: white;">'
    #                         "Voir le document</a>",
    #                         value,
    #                     )
    #             return data

    #         class Meta:
    #             proxy = True

    #     return CustomSubmission


class RecruitmentPage(Page):
    contract_type = models.ForeignKey(
        ContractType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recruitment_pages",
        verbose_name="Type de contrat",
    )
    job_title = models.CharField(max_length=255, verbose_name="Poste")
    location = models.CharField(max_length=255, blank=True, verbose_name="Localisation")
    body = RichTextField(blank=True, verbose_name="Description")
    salary = models.CharField(max_length=255, blank=True, verbose_name="Salaire")
    date = models.DateField(auto_now_add=True, verbose_name="Date")

    content_panels = Page.content_panels + [
        FieldPanel("contract_type"),
        FieldPanel("job_title"),
        # FieldPanel("introduction"),
        FieldPanel("location"),
        FieldPanel("body"),
        FieldPanel("salary"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        parent = self.get_parent().specific
        form = parent.get_form(request.POST or None, request.FILES or None)
        context["form"] = form
        if request.method == "POST" and form.is_valid():
            context["success"] = True

        return context

    class Meta:
        verbose_name = "Page Recrutement"

    parent_page_types = ["recruitment.RecruitmentIndexPage"]
    subpage_types = []
