import chromadb
from text_preprocessing import segmentation

client = chromadb.Client()
try:
    collection = client.create_collection("pdf")
except:
    collection = client.delete_collection("pdf")
    collection = client.create_collection("pdf")


def load_pdf(pdf1, pdf2):
    data = {}
    data[0] = segmentation(pdf1)
    data[1] = segmentation(pdf2)

    for i in range(2):
        print(f"Adding PDF {i+1} to collection")
        collection.add(
            ids=[f"pdf{i}_{j}" for j in range(len(data[i]))],
            documents=data[i],
            metadatas=[{"pdf": i} for _ in range(len(data[i]))],
        )


def query(query:str,n_results=15):
    results = collection.query([query], n_results=n_results)[0]
    
    output=[]
    for i in results:
        output.append(f"from Pdf {results["metadatas"][i]["pdf"]+1} : {results['documents'][i]}")
    
    return output