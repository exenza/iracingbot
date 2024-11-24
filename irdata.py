from iracingdataapi.client import irDataClient

irdata = irDataClient(username='massimo.berta@gmail.com', password='FuckW3b!massib80')

driverid=(irdata.lookup_drivers('Massimo Berta')[0]['cust_id'])
print(irdata.season_spectator_subsessionids([72327319]))
