from league.models import League

newLeague = League.objects.create(name="Test League 2")
print("success")