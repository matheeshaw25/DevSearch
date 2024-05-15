from django.http import JsonResponse # turns url routes to JSON format

#gets all the routes of urls and returns in JSON format
def getRoutes(request):

    routes=[
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'}, 
        {'POST':'/api/users/token/refresh'}, # when users token expries it keeps the user logged in job of 'refresh'
    ]

    return JsonResponse(routes, safe=False) # return part