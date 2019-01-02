from rest_framework import status, views
from Problematic.serializers import DataSourceSerializer
from rest_framework.response import Response
from Problematic.ModelTraining import createmodel
from Problematic.models import DataSource
from sklearn.externals import joblib
import pandas as pd
import os
import io
import datetime
import json


class DatasetView(views.APIView):

    def post(self, request):
        datasets = request.data.get('datasets')
        name = request.data.get('name')
        nature = request.content_type
        basepath = os.path.dirname(os.path.abspath('api_fichier.py'))
        libelle = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + '_' + name + '.json'
        filepath = basepath + "\Data\\" + libelle
        if nature == 'application/json':
            createfile(datasets, filepath)
        return Response({
            'libelle': libelle,
            'lien': filepath
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        lien = self.request.query_params.get('lien')
        if lien is None:
            data = {"error": "Aucun lien passé en parametres"}
            return Response({
                'data': data
            }, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = readfile(lien)
            return Response({
                'data': data
            }, status=status.HTTP_201_CREATED)


def createfile(data, filepath):
    basepath = os.path.dirname(os.path.abspath('api_fichier.py')) + '\\Data'
    if os.path.exists(basepath):
        with io.open(filepath, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)
    else:
        os.mkdir(basepath)
        with io.open(filepath, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)


def readfile(filepath):
    with open(filepath) as json_data:
        data_dict = json.load(json_data)
    return data_dict


class ModelTrainedView(views.APIView):

    def post(self, request):
        print("lancement du post")
        idproblematic = request.data.get('idproblematic')
        print(idproblematic)
        dataset = request.data.get('dataset')
        entree = request.data.get('entree')
        print(entree)
        sortie = request.data.get('sortie')
        print(sortie)
        percent = request.data.get('percent')
        print(percent)
        # precision = 73
        reponse = createmodel(idproblematic, dataset, entree, sortie, percent)
        print(reponse)
        return Response({
                'models': reponse
            }, status=status.HTTP_201_CREATED)


class ModelGeneratedView(views.APIView):

    def post(self, request, id, idmodel):
        idmodel = int(idmodel)
        typeml = 0
        queryset = DataSource.objects.get(id=id)
        serializer_class = DataSourceSerializer(queryset)
        data = serializer_class.data
        name = data['problematique']
        dataint = data['DataInt']
        if idmodel == 0:
            print('naive_bayes')
            typeml = 'naive_bayes'
        elif idmodel == 1:
            print('Kneighbors')
            typeml = 'Kneighbors'
        filename = os.path.dirname(os.path.abspath('api_fichier.py')) + '\\Models-Trained\\' + name + '\\' + typeml + '.pkl'
        print(filename)
        clf = joblib.load(filename)
        print(clf)
        # POST AN ARRAY OF DATA
        data = request.data
        data = data['data']
        print(data)
        data = prediction(clf, data, dataint)
        print(data)
        return Response({
            'reponse': data
        }, status=status.HTTP_201_CREATED)


def prediction(clf, data, dataint):
    data = json.dumps(data)
    df = pd.read_json(data)
    datavalue = df[dataint].values
    resultat = clf.predict(datavalue)
    return resultat

