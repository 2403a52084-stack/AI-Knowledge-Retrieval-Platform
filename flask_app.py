from flask import Flask, render_template, request, send_from_directory
import os
import sys
import uuid


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

# Create uploads folder automatically
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# ADD SRC TO PYTHON PATH
# ============================================================

if SRC_DIR not in sys.path:
    sys.path.insert(
        0,
        SRC_DIR
    )


# ============================================================
# IMPORT PROJECT MODULES
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

from agents.orchestrator import (
    MultiAgentOrchestrator
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================================================
# LOAD MODELS ONCE
# ============================================================

print("Loading embedding model...")

embedding_model = load_embedding_model()

print("Embedding model loaded successfully.")


print("Loading multi-agent system...")

orchestrator = MultiAgentOrchestrator()

print("Multi-agent system loaded successfully.")


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED_EXTENSIONS = {
    ".pdf": "PDF",
    ".docx": "DOCX",
    ".txt": "TXT",
    ".csv": "CSV"
}


# ============================================================
# HOME PAGE
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    answer = None

    sources = []

    message = None


    # ========================================================
    # POST REQUEST
    # ========================================================

    if request.method == "POST":

        action = request.form.get(
            "action"
        )


        # ====================================================
        # UPLOAD FOUR DOCUMENTS
        # ====================================================

        if action == "upload":

            files_to_process = [

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


            upload_results = []

            successful_count = 0


            # =================================================
            # PROCESS ALL FOUR FILES
            # =================================================

            for file_type, uploaded_file in files_to_process:

                # No file selected
                if (
                    uploaded_file is None
                    or uploaded_file.filename.strip() == ""
                ):

                    upload_results.append(
                        f"⚠️ {file_type}: No file selected."
                    )

                    continue


                original_filename = (
                    uploaded_file.filename
                )


                # ------------------------------------------------
                # Validate extension
                # ------------------------------------------------

                extension = os.path.splitext(
                    original_filename
                )[1].lower()


                if extension not in ALLOWED_EXTENSIONS:

                    upload_results.append(
                        f"❌ {original_filename}: "
                        f"Unsupported file type."
                    )

                    continue


                # ------------------------------------------------
                # Unique stored filename
                # ------------------------------------------------

                stored_filename = (
                    f"{uuid.uuid4().hex[:8]}_"
                    f"{original_filename}"
                )


                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    stored_filename
                )


                try:

                    # --------------------------------------------
                    # Save file
                    # --------------------------------------------

                    uploaded_file.save(
                        save_path
                    )


                    # --------------------------------------------
                    # Extract text
                    # --------------------------------------------

                    text = load_document(
                        save_path
                    )


                    # --------------------------------------------
                    # Clean text
                    # --------------------------------------------

                    text = clean_text(
                        text
                    )


                    # --------------------------------------------
                    # Create chunks
                    # --------------------------------------------

                    chunks = split_text(
                        text
                    )


                    if not chunks:

                        upload_results.append(
                            f"❌ {original_filename}: "
                            f"No text could be extracted."
                        )

                        continue


                    # --------------------------------------------
                    # Generate embeddings
                    # --------------------------------------------

                    embeddings = generate_embeddings(
                        embedding_model,
                        chunks
                    )


                    # --------------------------------------------
                    # Open ChromaDB
                    # --------------------------------------------

                    collection = create_vector_store()


                    # --------------------------------------------
                    # Unique document ID
                    # --------------------------------------------

                    document_id = (
                        uuid.uuid4().hex[:8]
                    )


                    # --------------------------------------------
                    # Metadata + IDs
                    # --------------------------------------------

                    metadatas = []

                    ids = []


                    for index in range(
                        len(chunks)
                    ):

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


                        ids.append(
                            f"{document_id}_{index}"
                        )


                    # --------------------------------------------
                    # Add chunks to ChromaDB
                    # --------------------------------------------

                    add_documents(
                        collection,
                        chunks,
                        embeddings,
                        metadatas,
                        ids
                    )


                    successful_count += 1


                    upload_results.append(
                        f"✅ <strong>{file_type}</strong> — "
                        f"{original_filename} — "
                        f"{len(chunks)} chunks indexed."
                    )


                except Exception as e:

                    upload_results.append(
                        f"❌ <strong>{file_type}</strong> — "
                        f"{original_filename} — "
                        f"Error: {e}"
                    )


            # =================================================
            # UPLOAD SUMMARY
            # =================================================

            if successful_count == 4:

                upload_results.append(
                    "<br>🎉 <strong>"
                    "All 4 documents were successfully "
                    "processed and indexed!"
                    "</strong>"
                )

            elif successful_count > 0:

                upload_results.append(
                    f"<br>⚠️ <strong>"
                    f"{successful_count} of 4 documents "
                    f"were successfully processed."
                    "</strong>"
                )

            else:

                upload_results.append(
                    "<br>❌ No documents were indexed."
                )


            message = "<br>".join(
                upload_results
            )


        # ====================================================
        # ASK QUESTION
        # ====================================================

        elif action == "ask":

            question = request.form.get(
                "question",
                ""
            ).strip()


            if not question:

                message = (
                    "❌ Please enter a question."
                )


            else:

                try:

                    # --------------------------------------------
                    # Multi-agent query processing
                    # --------------------------------------------

                    result = (
                        orchestrator.process_query(
                            question
                        )
                    )


                    # --------------------------------------------
                    # Answer
                    # --------------------------------------------

                    answer = result.get(
                        "answer",
                        "No answer generated."
                    )


                    # --------------------------------------------
                    # Retrieved results
                    # --------------------------------------------

                    retrieved_results = (
                        result.get(
                            "results",
                            []
                        )
                    )


                    for item in retrieved_results:

                        metadata = item.get(
                            "metadata",
                            {}
                        )


                        source = metadata.get(
                            "source",
                            "Unknown"
                        )


                        stored_filename = metadata.get(
                            "stored_filename",
                            ""
                        )


                        sources.append(
                            {
                                "source":
                                    source,

                                "stored_filename":
                                    stored_filename,

                                "distance":
                                    item.get(
                                        "distance",
                                        "N/A"
                                    )
                            }
                        )


                except Exception as e:

                    message = (
                        f"❌ Question processing error: {e}"
                    )


    # ========================================================
    # RENDER PAGE
    # ========================================================

    return render_template(
        "index.html",
        answer=answer,
        sources=sources,
        message=message
    )


# ============================================================
# OPEN RETRIEVED SOURCE
# ============================================================

@app.route(
    "/source/<path:filename>"
)
def open_source(filename):

    # Normalize Windows backslashes
    filename = filename.replace(
        "\\",
        "/"
    )


    # --------------------------------------------------------
    # Uploaded document
    # --------------------------------------------------------

    if "/" not in filename:

        uploaded_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if os.path.isfile(
            uploaded_path
        ):

            return send_from_directory(
                UPLOAD_FOLDER,
                filename
            )


    # --------------------------------------------------------
    # Existing project knowledge-base document
    # --------------------------------------------------------

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
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )