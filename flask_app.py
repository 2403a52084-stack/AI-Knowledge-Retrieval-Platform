import os
import sys
import uuid

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# PYTHON PATH
# ============================================================

if SRC_DIR not in sys.path:

    sys.path.insert(
        0,
        SRC_DIR
    )


# ============================================================
# PROJECT MODULES
# ============================================================

from document_loader import load_document
from text_cleaner import clean_text
from chunking import split_text

from embeddings import (
    load_embedding_model,
    generate_embeddings
)

from vector_store import (
    create_vector_store,
    add_documents
)

from agents.orchestrator import Orchestrator


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = load_embedding_model()

print("Embedding model loaded successfully.")


# ============================================================
# LOAD M2 ORCHESTRATOR
# ============================================================

print("Loading multi-agent system...")

orchestrator = Orchestrator()

print("Multi-agent system loaded successfully.")


# ============================================================
# HOME PAGE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    # Default values
    answer = None
    result = None
    message = None
    question = ""
    upload_results = []


    # ========================================================
    # GET
    # ========================================================

    if request.method == "GET":

        return render_template(
            "index.html",
            answer=None,
            result=None,
            message=None,
            question="",
            upload_results=[]
        )


    # ========================================================
    # POST ACTION
    # ========================================================

    action = request.form.get(
        "action",
        ""
    )


    # ========================================================
    # UPLOAD DOCUMENTS
    # ========================================================

    if action == "upload":

        files = [

            (
                "PDF",
                request.files.get(
                    "pdf_file"
                )
            ),

            (
                "DOCX",
                request.files.get(
                    "docx_file"
                )
            ),

            (
                "TXT",
                request.files.get(
                    "txt_file"
                )
            ),

            (
                "CSV",
                request.files.get(
                    "csv_file"
                )
            )

        ]


        success_count = 0


        for file_type, uploaded_file in files:

            # ------------------------------------------------
            # No file
            # ------------------------------------------------

            if (
                uploaded_file is None
                or not uploaded_file.filename
            ):

                upload_results.append(
                    f"⚠️ {file_type}: No file selected."
                )

                continue


            original_filename = (
                uploaded_file.filename
            )


            # ------------------------------------------------
            # Check extension
            # ------------------------------------------------

            extension = os.path.splitext(
                original_filename
            )[1].lower()


            if extension not in [
                ".pdf",
                ".docx",
                ".txt",
                ".csv"
            ]:

                upload_results.append(
                    f"❌ {original_filename}: "
                    f"Unsupported file type."
                )

                continue


            # ------------------------------------------------
            # Create unique stored filename
            # ------------------------------------------------

            stored_filename = (
                uuid.uuid4().hex[:8]
                + "_"
                + original_filename
            )


            save_path = os.path.join(
                UPLOAD_FOLDER,
                stored_filename
            )


            try:

                # ============================================
                # SAVE FILE
                # ============================================

                uploaded_file.save(
                    save_path
                )


                # ============================================
                # EXTRACT TEXT
                # ============================================

                text = load_document(
                    save_path
                )


                # ============================================
                # CLEAN TEXT
                # ============================================

                text = clean_text(
                    text
                )


                # ============================================
                # CHUNK TEXT
                # ============================================

                chunks = split_text(
                    text
                )


                if not chunks:

                    upload_results.append(
                        f"❌ {original_filename}: "
                        f"No text could be extracted."
                    )

                    continue


                # ============================================
                # GENERATE EMBEDDINGS
                # ============================================

                embeddings = generate_embeddings(
                    embedding_model,
                    chunks
                )


                # ============================================
                # VECTOR STORE
                # ============================================

                collection = create_vector_store()


                # ============================================
                # DOCUMENT ID
                # ============================================

                document_id = (
                    uuid.uuid4().hex[:8]
                )


                ids = []
                metadatas = []


                for index in range(
                    len(chunks)
                ):

                    ids.append(
                        f"{document_id}_{index}"
                    )


                    metadatas.append(
                        {
                            "source":
                                original_filename,

                            "stored_filename":
                                stored_filename,

                            "file_type":
                                file_type,

                            "chunk_index":
                                index,

                            "document_id":
                                document_id
                        }
                    )


                # ============================================
                # ADD TO CHROMADB
                # ============================================

                add_documents(
                    collection,
                    chunks,
                    embeddings,
                    metadatas,
                    ids
                )


                success_count += 1


                upload_results.append(
                    f"✅ <strong>{file_type}</strong>: "
                    f"{original_filename} "
                    f"— {len(chunks)} chunks indexed."
                )


            except Exception as error:

                upload_results.append(
                    f"❌ <strong>{file_type}</strong>: "
                    f"{original_filename} "
                    f"— {error}"
                )


        # ====================================================
        # UPLOAD SUMMARY
        # ====================================================

        if success_count == 4:

            upload_results.append(
                "<br>🎉 <strong>"
                "All 4 documents were successfully "
                "processed and indexed!"
                "</strong>"
            )

        elif success_count > 0:

            upload_results.append(
                f"<br>⚠️ <strong>"
                f"{success_count} of 4 documents "
                f"were successfully indexed."
                "</strong>"
            )

        else:

            upload_results.append(
                "<br>❌ <strong>"
                "No documents were indexed."
                "</strong>"
            )


        return render_template(
            "index.html",
            answer=None,
            result=None,
            message=None,
            question="",
            upload_results=upload_results
        )


    # ========================================================
    # ASK QUESTION
    # ========================================================

    if action == "ask":

        question = request.form.get(
            "question",
            ""
        ).strip()


        if not question:

            return render_template(
                "index.html",
                answer=None,
                result=None,
                message="❌ Please enter a question.",
                question="",
                upload_results=[]
            )


        try:

            # ================================================
            # M2 MULTI-AGENT PIPELINE
            # ================================================

            result = orchestrator.process_query(
                question
            )


            answer = result.get(
                "answer",
                "No answer generated."
            )


            return render_template(
                "index.html",
                answer=answer,
                result=result,
                message=None,
                question=question,
                upload_results=[]
            )


        except Exception as error:

            return render_template(
                "index.html",
                answer=None,
                result=None,
                message=(
                    f"❌ Question processing error: "
                    f"{error}"
                ),
                question=question,
                upload_results=[]
            )


    # ========================================================
    # UNKNOWN ACTION
    # ========================================================

    return render_template(
        "index.html",
        answer=None,
        result=None,
        message="❌ Unknown action.",
        question=question,
        upload_results=[]
    )


# ============================================================
# SOURCE FILE ROUTE
# ============================================================

@app.route(
    "/source/<path:filename>",
    methods=["GET"]
)
def source(filename):

    # Convert URL slash to Windows slash
    filename = filename.replace(
        "/",
        os.sep
    )


    # ========================================================
    # CHECK UPLOADED FILE
    # ========================================================

    uploaded_name = os.path.basename(
        filename
    )

    uploaded_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_name
    )


    if os.path.isfile(
        uploaded_path
    ):

        return send_from_directory(
            UPLOAD_FOLDER,
            uploaded_name
        )


    # ========================================================
    # CHECK ORIGINAL PROJECT FILE
    # Example:
    # data/technology/artificial_intelligence.pdf
    # ========================================================

    project_file = os.path.abspath(
        os.path.join(
            BASE_DIR,
            filename
        )
    )


    project_root = os.path.abspath(
        BASE_DIR
    )


    # Security check
    if not project_file.startswith(
        project_root + os.sep
    ):

        return (
            "Invalid source path.",
            403
        )


    if os.path.isfile(
        project_file
    ):

        directory = os.path.dirname(
            project_file
        )

        file_name = os.path.basename(
            project_file
        )

        return send_from_directory(
            directory,
            file_name
        )


    return (
        "Source file not found.",
        404
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return {
        "status": "ok",
        "service": "AI Knowledge Retrieval Platform"
    }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )