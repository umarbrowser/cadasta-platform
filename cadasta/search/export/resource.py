import json
import os
import subprocess

from openpyxl import Workbook
from zipfile import ZipFile

from resources.models import ContentObject

MIME_TYPE = 'application/zip'


class ResourceExporter():

    def __init__(self, project):
        self.project = project

    def make_download(self, es_dump_path):
        base_path = os.path.splitext(es_dump_path)[0]

        # Create worksheet for resources metadata
        xls_path = base_path + '-res.xlsx'
        workbook = Workbook(write_only=True)
        worksheet = workbook.create_sheet(title='resources')
        worksheet.append(['id', 'name', 'description', 'filename',
                          'locations', 'parties', 'relationships'])

        # Create temp dir where S3 files will be downloaded
        dir_path = base_path + '-res-dir'
        os.makedirs(dir_path)

        # Create zip file and start processing
        zip_path = base_path + '-res.zip'
        with ZipFile(zip_path, 'a') as myzip:

            f = open(es_dump_path, encoding='utf-8')
            while True:
                # Read 2 lines in the dump file
                type_line = f.readline()
                source_line = f.readline()
                if not type_line:
                    break

                # Extract ES type and source and skip if not resource
                es_type = json.loads(type_line)['index']['_type']
                if es_type != 'resource':
                    continue
                source = json.loads(source_line)

                # Fetch file from ES using curl and add to zip file
                temp_resource_path = dir_path + '/' + source['original_file']
                url = source['file']
                if url[0] == '/':
                    url = 'http://localhost:8000' + url
                subprocess.run([
                    'curl', '-o', temp_resource_path, '-XGET', url
                ])
                myzip.write(temp_resource_path,
                            arcname=source['original_file'])

                self.append_resource_metadata(source, worksheet)

            workbook.save(filename=xls_path)

            myzip.write(xls_path, arcname='resources.xlsx')
            myzip.close()

        return zip_path, MIME_TYPE

    def append_resource_metadata(self, source, worksheet):
        locations = []
        parties = []
        tenure_rels = []

        links = ContentObject.objects.filter(
            resource__id=source['id']).values_list(
                'content_type__model', 'object_id')
        for link in links:
            if link[0] == 'spatialunit':
                locations.append(link[1])
            elif link[0] == 'party':
                parties.append(link[1])
            elif link[0] == 'tenurerelationship':
                tenure_rels.append(link[1])

        worksheet.append([
            source['id'],
            source['name'],
            source['description'],
            source['original_file'],
            ', '.join(locations),
            ', '.join(parties),
            ', '.join(tenure_rels),
        ])
