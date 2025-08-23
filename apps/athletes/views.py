from rest_framework import viewsets,permissions
from .serializers import AthleteSerializer,PublicAthleteSerializer
from .models import Athlete
from .permissions import ReceptionistCreateReadOrManagerReadOnlyOrAthleteOrCoachReadOnly 
from .filters import AthleteFilter
from django.db.models import Prefetch
from apps.reservations.models import Reservation
from apps.sporthistories.models import SportHistory
from apps.athletes.services import delete_athlete

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers



class AthleteViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user=self.request.user
        if user.role =='coach':
            return Athlete.objects.all()
        elif user.role in ['manager','receptionist']:
            return Athlete.objects.all().prefetch_related(Prefetch('reserves',queryset=Reservation.objects.all().only('public_id')))\
                        .prefetch_related(Prefetch('sport_histories',queryset=SportHistory.objects.all().only('public_id')))
        
        return Athlete.objects.filter(public_id=user.public_id)\
                    .prefetch_related(Prefetch('reserves',queryset=Reservation.objects.filter(athlete__public_id=user.public_id)\
                                               .only('public_id')))\
                        .prefetch_related(Prefetch('sport_histories',queryset=SportHistory.objects.filter(athlete__public_id=user.public_id)\
                                                   .only('public_id')))


    @method_decorator(cache_page(60 * 15,key_prefix='athlete-list'))  
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
                                                 

    def get_serializer_class(self):
        if self.request.user.role=='coach':
            return PublicAthleteSerializer
        return AthleteSerializer
    
    permission_classes=[permissions.IsAuthenticated,ReceptionistCreateReadOrManagerReadOnlyOrAthleteOrCoachReadOnly]
    lookup_field='public_id'
    filterset_class=AthleteFilter


    def perform_destroy(self, instance):
        delete_athlete(instance)

    