import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.naive_bayes import GaussianNB
from sklearn import neighbors
from sklearn.externals import joblib
from sklearn import metrics
from Problematic.models import DataSource
from Problematic.serializers import DataSourceSerializer


def createmodel(idproblematic, dataset, entree, sortie, test_percent, dataset_test):
    reponse = []
    queryset = DataSource.objects.get(id=idproblematic)
    serializer_class = DataSourceSerializer(queryset)
    getproblematic = serializer_class.data
    problematicname = getproblematic['problematique']
    data = json.dumps(dataset)
    df = pd.read_json(data)
    dataint = entree
    dataout = [sortie]
    x = df[dataint].values
    y = df[dataout].values

    # Cas où le jeu de données de test n'est pas contenu dans le jeu de données global
    if test_percent == 0:
        data_test = json.dumps(dataset_test)
        df_test = pd.read_json(data_test)
        x_test = df_test[dataint].values
        y_test = df_test[dataout].values
        x_train = x
        y_train = y
    else:
        test_size = test_percent
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)

    fill_0 = SimpleImputer(missing_values=0, strategy="mean")
    x_train = fill_0.fit_transform(x_train)
    x_test = fill_0.fit_transform(x_test)
    filename = os.path.dirname(os.path.abspath('api_fichier.py')) + '\\Models-Trained\\' + problematicname

    # Algorithm de Gauss
    clf = GaussianNB()
    clf.fit(x_train, y_train.ravel())
    result = clf.predict(x_test)
    precision = metrics.accuracy_score(y_test, result) * 100
    api = 'api/Problematics/' + idproblematic + '/ModelTrained/0'
    print(api)
    reponse.append({'api': api, 'precision': precision})
    typeml = 'naive_bayes'
    createfile(clf, filename, typeml)

    # Algorithm de Neighbors
    clf = neighbors.KNeighborsClassifier(n_neighbors=8)
    clf.fit(x_train, y_train.ravel())
    result = clf.predict(x_test)
    precision = metrics.accuracy_score(y_test, result) * 100
    api = 'api/Problematics/' + idproblematic + '/ModelTrained/1'
    print(api)
    reponse.append({'api': api, 'precision': precision})
    typeml = 'Kneighbors'
    createfile(clf, filename, typeml)

    return reponse


def createfile(model, basepath, typeml):
    filename = basepath + '\\' + typeml + '.pkl'
    if os.path.exists(basepath):
        joblib.dump(model, filename)

    else:
        os.mkdir(basepath)
        joblib.dump(model, filename)
