from flask import Flask, make_response, jsonify
from domain.usecases.ipi_usecase import IpiUseCase

app = Flask(__name__)
ipi_usecase = IpiUseCase()

@app.route('/process_ipi', methods = ['GET'])
def process():
    try:
        ipi_usecase.process_ipi()
        return make_response(jsonify({"message": "IPI process ended!"}))
    except (Exception) as error:
        print(f"Error processing IPI!: {error}")
        return make_response(jsonify({"message": "Error processing IPI!", "error": error}))

app.run(host="0.0.0.0", port=5000)