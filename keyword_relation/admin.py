from django.contrib import admin
from .models import Keyword_Pages
from .models import User_Validation
from .models import User_Validation_Summary
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q
from django.db.models.functions import Trunc
from django.db.models import DateTimeField

admin.site.register(Keyword_Pages)
admin.site.register(User_Validation)


@admin.register(User_Validation_Summary)
class User_Validation_Summary_Admin(admin.ModelAdmin):
    change_list_template = 'admin/user_val_summary_change_list.html'
    # date_hierarchy = 'created'

    list_filter = (
        'main_keyword',
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('task_id'),
            'total_domain_classified': Sum('domainness_belongs_to_domain'),
            # 'total_positive_classified': Count('domainness_belongs_to_domain', filter=Q(domainness_belongs_to_domain=1)),
            # 'total_negative_classified': Count('domainness_belongs_to_domain', filter=Q(domainness_belongs_to_domain=0)),
        }

        response.context_data['summary'] = list(
            qs
            .values('main_keyword')
            .annotate(**metrics)
            .order_by('main_keyword')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        # summary_over_time = qs.annotate(
        #     period=Trunc(
        #         'time_stamp',
        #         'day',
        #         output_field=DateTimeField(),
        #     ),
        # ).values('time_stamp').annotate(total=Sum('domainness_belongs_to_domain')).order_by('time_stamp')

        # summary_range = summary_over_time.aggregate(
        #     low=Min('total'),
        #     high=Max('total'),
        # )
        # high = summary_range.get('high', 0)
        # low = summary_range.get('low', 0)

        # response.context_data['summary_over_time'] = [{
        #     'period': x['time_stamp'],
        #     'total': x['domainness_belongs_to_domain'] or 0,
        #     'pct': \
        #        ((x['total'] or 0) - low) / (high - low) * 100
        #        if high > low else 0,
        # } for x in summary_over_time]

        return response