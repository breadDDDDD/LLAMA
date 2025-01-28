from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger, swag_from
import os
import ollama

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3
}
swagger = Swagger(app)

class LLAMA(Resource):
    @swag_from({
        'responses': {
            200: {'description': 'prompt successfully'},
            400: {'description': 'error'}
        },
        'parameters': [
            {
                'name': 'Prompt Chatbot',
                'in': 'body',
                'required': True,
                'description': 'write prompt',
                'schema': {
                    'type': 'object',
                    'properties': {
                        
                        'prompt': {'type': 'string'}
                    },
                    'required': [ 'prompt']
                }
            }
        ]
    })
    def post(self):
        response_llm = ollama.chat(
            model="sharkboo",
            messages=[
                {"role": "user", "content": "prompt"}
                ]
        )
        return response_llm["message"]["content"]

class FileUpload(Resource):
    @swag_from({
        'responses': {
            200: {'description': 'Success'},
            404: {'description': 'File not found'}
        },
        
    })
    
    def get(self):
        uploads_dir = 'data'
        files = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
        return{"files": files}, 200

        
    @swag_from({
        'responses': {
            200: {'description': 'File uploaded successfully'},
            400: {'description': 'Error in file upload'}
        },
        'parameters': [
            {
                'name': 'Post file',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description': 'Upload a file',
            }
        ]
    })
    
    def post(self):
        file = request.files['file']

        if file.filename == '':
            return {"error": "No selected file"}, 400

        save_path = os.path.join('data', file.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)

        return {"message": f"File saved to {save_path}"}, 200
    
    @swag_from({
            'responses': {
                200: {'description': 'Success'},
                404: {'description': 'File not found'}
            },
            'parameters': [
                {
                    'name': 'Delete filename',
                    'in': 'query',
                    'type': 'string',
                    'required': True,
                    'description': 'Name file',
                }
            ]
        })
    def delete(self):
        dir = 'data'
        file = request.args.get('filename')
        if file:
            file_path = os.path.join(dir, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                return {"filename": file, "message": "File deleted"}, 200
            else:
                return {"error": f"File {file} not found"}, 404
        else:
            if not os.path.exists(dir):
                return {"error": "Uploads directory does not exist"}, 404

api.add_resource(LLAMA, '/LLAMAChat')
api.add_resource(FileUpload, '/Upload')




if __name__ == '__main__':
    app.run(debug=True)