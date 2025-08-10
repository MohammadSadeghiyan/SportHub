from .models import Excersice

class ExcersiceService:
    
    def __init__(self,validated_data,sport_history):
        self.validated_data=validated_data
        self.sport_history=sport_history
    
    def create_excersice(self):
        excersice=Excersice.objects.create(**self.validated_data,sport_history=self.sport_history)
        excersice.save()
        return excersice

        