import os
import sys
import uuid

from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    session
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

# Needed for storing pending clarification queries
app.secret_key = (
    "ai-knowledge-retrieval-m3-secret-key"
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = load_embedding_model()

print("Embedding model loaded successfully.")


# ============================================================
# LOAD MULTI-AGENT ORCHESTRATOR
# ============================================================

print("Loading multi-agent system...")

orchestrator = Orchestrator()

print("Multi-agent system loaded successfully.")


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_memory_data():

    history = (
        orchestrator.memory_agent.get_history()
    )

    size = (
        orchestrator.memory_agent.memory_size()
    )

    return history, size


# ============================================================
# HOME PAGE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    answer = None
    result = None
    message = None
    question = ""
    upload_results = []

    clarification_question = None
    pending_query = None


    # ========================================================
    # CURRENT MEMORY
    # ========================================================

    memory_history, memory_size = (
        get_memory_data()
    )


    # ========================================================
    # GET REQUEST
    # ========================================================

    if request.method == "GET":

        return render_template(
            "index.html",
            answer=None,
            result=None,
            message=None,
            question="",
            upload_results=[],
            clarification_question=None,
            pending_query=None,
            memory_history=memory_history,
            memory_size=memory_size
        )


    # ========================================================
    # GET ACTION
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
            # CHECK FILE
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
            # VALIDATE EXTENSION
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
            # UNIQUE STORED FILENAME
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
                # LOAD DOCUMENT
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
                # SPLIT INTO CHUNKS
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
                # CREATE VECTOR STORE
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


                # ============================================
                # METADATA
                # ============================================

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
                    f"— Error: {error}"
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


        memory_history, memory_size = (
            get_memory_data()
        )


        return render_template(
            "index.html",
            answer=None,
            result=None,
            message=None,
            question="",
            upload_results=upload_results,
            clarification_question=None,
            pending_query=None,
            memory_history=memory_history,
            memory_size=memory_size
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
                upload_results=[],
                clarification_question=None,
                pending_query=None,
                memory_history=memory_history,
                memory_size=memory_size
            )


        try:

            # ================================================
            # PROCESS THROUGH ORCHESTRATOR
            # ================================================

            result = orchestrator.process_query(
                question
            )


            # ================================================
            # CHECK CLARIFICATION
            # ================================================

            if result.get(
                "status"
            ) == "clarification_required":

                clarification = result.get(
                    "clarification",
                    {}
                )


                clarification_question = (
                    clarification.get(
                        "follow_up_question",
                        "Could you provide more details?"
                    )
                )


                # Store pending original query
                session["pending_query"] = (
                    question
                )


                # Refresh memory information
                memory_history, memory_size = (
                    get_memory_data()
                )


                return render_template(
                    "index.html",
                    answer=None,
                    result=result,
                    message=None,
                    question=question,
                    upload_results=[],
                    clarification_question=(
                        clarification_question
                    ),
                    pending_query=question,
                    memory_history=memory_history,
                    memory_size=memory_size
                )


            # ================================================
            # NORMAL RESPONSE
            # ================================================

            answer = result.get(
                "answer",
                "No answer generated."
            )


            memory_history, memory_size = (
                get_memory_data()
            )


            return render_template(
                "index.html",
                answer=answer,
                result=result,
                message=None,
                question=question,
                upload_results=[],
                clarification_question=None,
                pending_query=None,
                memory_history=memory_history,
                memory_size=memory_size
            )


        except Exception as error:

            memory_history, memory_size = (
                get_memory_data()
            )


            return render_template(
                "index.html",
                answer=None,
                result=None,
                message=(
                    f"❌ Question processing error: "
                    f"{error}"
                ),
                question=question,
                upload_results=[],
                clarification_question=None,
                pending_query=None,
                memory_history=memory_history,
                memory_size=memory_size
            )


    # ========================================================
    # CLARIFICATION RESPONSE
    # ========================================================

    if action == "clarify":

        clarification_response = (
            request.form.get(
                "clarification_response",
                ""
            ).strip()
        )


        pending_query = (
            session.get(
                "pending_query",
                ""
            ).strip()
        )


        # ----------------------------------------------------
        # CHECK PENDING QUERY
        # ----------------------------------------------------

        if not pending_query:

            return render_template(
                "index.html",
                answer=None,
                result=None,
                message=(
                    "❌ No pending question was found."
                ),
                question="",
                upload_results=[],
                clarification_question=None,
                pending_query=None,
                memory_history=memory_history,
                memory_size=memory_size
            )


        # ----------------------------------------------------
        # CHECK CLARIFICATION RESPONSE
        # ----------------------------------------------------

        if not clarification_response:

            return render_template(
                "index.html",
                answer=None,
                result=None,
                message=(
                    "❌ Please provide the clarification."
                ),
                question=pending_query,
                upload_results=[],
                clarification_question=(
                    "Please provide more details."
                ),
                pending_query=pending_query,
                memory_history=memory_history,
                memory_size=memory_size
            )


        try:

            # ================================================
            # PROCESS REFINED QUERY
            # ================================================

            result = orchestrator.process_query(
                pending_query,
                clarification_response
            )


            # ================================================
            # CLEAR PENDING QUERY
            # ================================================

            session.pop(
                "pending_query",
                None
            )


            answer = result.get(
                "answer",
                "No answer generated."
            )


            memory_history, memory_size = (
                get_memory_data()
            )


            return render_template(
                "index.html",
                answer=answer,
                result=result,
                message=None,
                question=result.get(
                    "refined_query",
                    pending_query
                ),
                upload_results=[],
                clarification_question=None,
                pending_query=None,
                memory_history=memory_history,
                memory_size=memory_size
            )


        except Exception as error:

            memory_history, memory_size = (
                get_memory_data()
            )


            return render_template(
                "index.html",
                answer=None,
                result=None,
                message=(
                    f"❌ Clarification processing error: "
                    f"{error}"
                ),
                question=pending_query,
                upload_results=[],
                clarification_question=None,
                pending_query=None,
                memory_history=memory_history,
                memory_size=memory_size
            )


    # ========================================================
    # UNKNOWN ACTION
    # ========================================================

    memory_history, memory_size = (
        get_memory_data()
    )


    return render_template(
        "index.html",
        answer=None,
        result=None,
        message="❌ Unknown action.",
        question="",
        upload_results=[],
        clarification_question=None,
        pending_query=None,
        memory_history=memory_history,
        memory_size=memory_size
    )


# ============================================================
# SOURCE FILE ROUTE
# ============================================================

@app.route(
    "/source/<path:filename>",
    methods=["GET"]
)
def source(filename):

    # Normalize path
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


    # ========================================================
    # SECURITY CHECK
    # ========================================================

    if not project_file.startswith(
        project_root + os.sep
    ):

        return (
            "Invalid source path.",
            403
        )


    # ========================================================
    # SERVE FILE
    # ========================================================

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
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )