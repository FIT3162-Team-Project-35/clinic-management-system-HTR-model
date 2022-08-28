import sys
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json

data = []


def main(Form,output_File):
    try:
        form_endpoint = "https://southeastasia.api.cognitive.microsoft.com/"
        form_key = "3b90ce02fdac44b2abbe51b1bc139a98"


        document_analysis_client = DocumentAnalysisClient(
            endpoint=form_endpoint, credential=AzureKeyCredential(form_key))


        
        with open(Form, "rb") as f:
            poller = document_analysis_client.begin_analyze_document(
                model_id="Model_2", document=f)

        result=poller.result()
        lst=[]
        for idx, document in enumerate(result.documents):
            print("--------Analyzing document #{}--------".format(idx + 1))
            print("Document has type {}".format(document.doc_type))
            print("Document has confidence {}".format(document.confidence))
            print("Document was analyzed by model with ID {}".format(result.model_id))
            for name, field in document.fields.items():
                field_value = field.value if field.value else field.content
                print("......found field of type '{}' with value '{}' and with confidence {}".format(field.value_type, field_value, field.confidence))
                lst+=[field_value]

        patient_info={
            "f_name":lst[0],
            "l_name":lst[1],
            "gender":lst[2],
            "telephone":lst[3],
            "address":lst[4],
            "city":lst[5],
            "post_code":lst[6],
            "date_of_birth":lst[7],
            "ec_f_name":lst[8],
            "ec_l_name":lst[9],
            "ec_telephone":lst[10],
            "ec_relationship":lst[11],
            "med_details":lst[12],
            "allergy_details":lst[13]
            }
        
        with open(output_File,"w")as outfile:
            json.dump(patient_info,outfile)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    form = sys.argv[1]
    outputFile=sys.argv[2]
    main(form,outputFile)