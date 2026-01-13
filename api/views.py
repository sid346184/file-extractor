from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import json
from .utils import process_directory

class ExtractTextView(APIView):
    def post(self, request):
        directory_path = request.data.get('directory_path')
        if not directory_path:
            return Response({"error": "directory_path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Make sure directory exists, etc. - handled by utils but good to have safety here
        if not os.path.exists(directory_path):
             return Response({"error": "Directory does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Process
        result = process_directory(directory_path)
        
        if "error" in result:
             if "not exist" in result["error"] or "not a directory" in result["error"]:
                 return Response(result, status=status.HTTP_400_BAD_REQUEST)
             return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(result, status=status.HTTP_200_OK)

    def get(self, request):
        output_file = 'output.json'
        if not os.path.exists(output_file):
            return Response({"error": "No output file found. Run POST first."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to read output file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
