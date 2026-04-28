from api.models import Plage

class PlageRepository:
    def get_plage_by_id(self, plage_id):
        try:
            return Plage.objects.get(pk=plage_id)
        except Plage.DoesNotExist:
            return None
        
    def get_plages_for_event(self, event_id):
        return Plage.objects.filter(event=event_id)