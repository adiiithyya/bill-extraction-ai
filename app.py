import json
import os
import tempfile

import streamlit as st

from extractor import extract_bill
from validator import validate_bill


st.set_page_config(
    page_title="Bill Extraction AI",
    page_icon="🧾",
    layout="wide"
)


st.title("🧾 Bill Extraction AI")
st.caption(
    "Extract structured information from bill images using multimodal AI."
)

st.divider()


uploaded_file = st.file_uploader(
    "Upload a bill image",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG and PNG"
)


if uploaded_file is not None:

    left, right = st.columns(2)

    with left:
        st.subheader("Uploaded Bill")
        st.image(
            uploaded_file,
            use_container_width=True
        )

    with right:
        st.subheader("Extraction")

        st.write(
            f"**File:** {uploaded_file.name}"
        )

        if st.button(
            "🔍 Extract Bill",
            type="primary",
            use_container_width=True
        ):

            temp_path = None

            try:
                # Create a temporary file for the uploaded image
                suffix = os.path.splitext(uploaded_file.name)[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(uploaded_file.getbuffer())
                    temp_path = temp_file.name

                with st.spinner(
                    "Analyzing bill with AI..."
                ):
                    bill = extract_bill(temp_path)

                st.session_state["bill"] = bill

            except Exception as e:
                st.error(
                    "Bill extraction failed."
                )

                st.caption(
                    "The AI service may be temporarily unavailable "
                    "or its API quota may have been exceeded."
                )

                st.code(str(e))

            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)


# Display results if extraction was successful
if "bill" in st.session_state:

    bill = st.session_state["bill"]

    st.divider()

    st.subheader("📋 Bill Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Vendor",
            bill.vendor_name or "Not available"
        )

    with col2:
        st.metric(
            "Invoice Number",
            bill.invoice_number or "Not available"
        )

    with col3:
        st.metric(
            "Date",
            bill.date or "Not available"
        )


    st.subheader("💰 Amount Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Subtotal",
            f"₹{bill.subtotal:.2f}"
            if bill.subtotal is not None
            else "Not available"
        )

    with col2:
        st.metric(
            "Tax",
            f"₹{bill.tax:.2f}"
            if bill.tax is not None
            else "Not available"
        )

    with col3:
        st.metric(
            "Discount",
            f"₹{bill.discount:.2f}"
            if bill.discount is not None
            else "Not available"
        )

    with col4:
        st.metric(
            "Total",
            f"₹{bill.total:.2f}"
            if bill.total is not None
            else "Not available"
        )


    st.subheader("🛒 Items")

    item_rows = []

    for item in bill.items:
        item_rows.append(
            {
                "Item": item.name,
                "Quantity": item.quantity,
                "Unit Price": f"₹{item.unit_price:.2f}",
                "Total": f"₹{item.total:.2f}",
            }
        )

    st.dataframe(
        item_rows,
        use_container_width=True,
        hide_index=True
    )


    st.subheader("✅ Validation")

    errors = validate_bill(bill)

    if errors:
        st.warning(
            "Some financial validation checks failed."
        )

        for error in errors:
            st.write(f"- {error}")

    else:
        st.success(
            "Financial validation successful!"
        )


    st.subheader("📥 Export")

    json_data = json.dumps(
        bill.model_dump(),
        indent=2
    )

    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="bill_extraction.json",
        mime="application/json",
        use_container_width=True
    )