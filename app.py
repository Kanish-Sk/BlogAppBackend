from bson import ObjectId
from flask import Flask, Response, jsonify, request
import json, os
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


def create_app():

    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000", "https://react-dojo-blog-website.netlify.app/"])

    mongo = MongoClient(os.getenv("MONGODB_URI"))
    db = mongo["react_blog"]


    ################################ home page #####################################

    @app.route('/home', methods=["GET"])
    def home():
        blogs_details = list(db.blogs.find({}))
        for blog in blogs_details:
            blog["_id"] = str(blog["_id"])
        return Response(
            response=json.dumps(blogs_details, default=str),
            status=200,
            mimetype="application/json"
        )

    ################################ create blog page #####################################

    @app.route('/createblog', methods=["POST"])
    def createblog():
        blogs = db["blogs"]
        if request.json:
            data = request.json
            print(data)
            blogs.insert_one(data)
            
        return jsonify({"message" : "blog added"})
        
    ################################ diplay each blog page #####################################

    @app.route('/blogs/<string:blog_id>', methods=["GET"])
    def get_blog(blog_id):
        blog = db["blogs"].find_one({"_id": ObjectId(blog_id)})
        blog["_id"] = str(blog["_id"])

        return Response(
            response=json.dumps(blog),
            status=200,
            mimetype="application/json"
        )

    ################################ delte blog #####################################

    @app.route('/blogs/<string:blog_id>', methods=["DELETE"])
    def delete_blog(blog_id):
        try:
            result = db["blogs"].delete_one({"_id": ObjectId(blog_id)})
            if result.deleted_count > 0:
                return Response(
                response="Blog deleted",
                status=200,
                mimetype="application/json"
            )
            else:
                return Response(
                response="Blog not found",
                status=500,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response="Can't delete blog",
                status=500,
                mimetype="application/json"
            )
    
    return app
