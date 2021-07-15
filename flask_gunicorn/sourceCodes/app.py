from flask import Flask
from flask.json import jsonify, jsonify, request
from models.all_models import ClassificationModel

# set up the models  
defaultModels = {
    'hosp_flag': {
		'name': 'hosp_flag',
		'modelPath': './trainedModels/trained_xgboost_model.pkl',
		'features': ['age', 'sshx_data_abn_lung_asc', 'sshx_data_altered_mental_state', 'sshx_data_headache', 'sshx_data_hypotension', 'sshx_data_irritability_cnfsn', 
                 'sshx_data_loss_of_taste_smell', 'sshx_data_malaise', 'sshx_data_myalgia', 'sshx_data_nasal_congestion', 'sshx_data_nausea',
                 'sshx_data_nose_bleed', 'sshx_data_pain', 'sshx_data_pharyngeal_exudate', 'sshx_data_prostration', 'sshx_data_rhinorrhea',
                 'sshx_data_seizures', 'sshx_data_difficulty_breathing', 'sshx_data_sneezing', 'sshx_data_sore_throat', 
                 'sshx_data_tachypnea', 'sshx_data_vomiting', 'sshx_data_other', 'ch_mi', 'ch_chf', 'ch_pvd', 'ch_cevd', 
                 'ch_dementia', 'ch_cpd', 'ch_rheumatic', 'ch_pud', 'ch_paraplegia', 'ch_rd', 'ch_cancer', 'ch_mets', 'diabetes', 'liver']
	}
	# 'icu_flag': {
	# 	'name': 'icu_flag',
	# 	'modelPath': './trainedModels/trained_xgboost_model_icu.pkl',
	# 	'features': ['age', 'sshx_data_abn_lung_asc', 'sshx_data_altered_mental_state', 'sshx_data_headache', 'sshx_data_hypotension', 'sshx_data_irritability_cnfsn', 
    #              'sshx_data_loss_of_taste_smell', 'sshx_data_malaise', 'sshx_data_myalgia', 'sshx_data_nasal_congestion', 'sshx_data_nausea',
    #              'sshx_data_nose_bleed', 'sshx_data_pain', 'sshx_data_pharyngeal_exudate', 'sshx_data_prostration', 'sshx_data_rhinorrhea',
    #              'sshx_data_seizures', 'sshx_data_difficulty_breathing', 'sshx_data_sneezing', 'sshx_data_sore_throat', 
    #              'sshx_data_tachypnea', 'sshx_data_vomiting', 'sshx_data_other', 'ch_mi', 'ch_chf', 'ch_pvd', 'ch_cevd', 
    #              'ch_dementia', 'ch_cpd', 'ch_rheumatic', 'ch_pud', 'ch_paraplegia', 'ch_rd', 'ch_cancer', 'ch_mets', 'diabetes', 'liver']
	# }
}

#create the modal objects
models = [ClassificationModel(model['name'], model['modelPath'], model['features']) for model in (list(defaultModels.values()))]
application = Flask(__name__)


@application.route("/", methods=['GET'])
@application.route("/home", methods=['GET'])
def home():
    return "Api is Up !!"

@application.route("/predict", methods=['POST'])
def predict():
    testingLabel = 'hosp_flag'
    requestBody = request.json
    selectedModel: ClassificationModel = [model for model in models if model.name == testingLabel][0]
    formattedInputData = selectedModel.getTestData(requestBody)
    predictionResults = selectedModel.predictNew(formattedInputData)
    listResult = predictionResults.tolist()
    return jsonify(listResult)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
