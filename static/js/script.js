document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const submitButton = document.getElementById("submitBtn");
    const buttonText = document.getElementById("buttonText");
    const spinner = document.getElementById("spinner");
    const outputDiv = document.getElementById("output");
    const segmentedImage = document.getElementById("segmentedImage");
    const message = document.getElementById("message");

    // Hide segmented image initially
    segmentedImage.style.display = "none";

    // Hide previous image when a new file is selected
    fileInput.addEventListener("change", function () {
        segmentedImage.style.display = "none";  // Hide previous image
        segmentedImage.src = "";  // Clear image source
        message.innerHTML = "";
        submitButton.disabled = !fileInput.files.length;
    });

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        const file = fileInput.files[0];

        if (!file) {
            message.innerHTML = `<p style="color:red;">❌ Please select a file first.</p>`;
            return;
        }

        // Disable button and show loading spinner
        submitButton.disabled = true;
        buttonText.style.display = "none";
        spinner.style.display = "inline";

        let formData = new FormData();
        formData.append("image", file);

        try {
            let response = await fetch("/segment", {
                method: "POST",
                body: formData
            });
        
            let data = await response.json();
            console.log("Response Data:", data);  // Debugging log
        
            if (!response.ok) {
                throw new Error(data.error || "Server returned an error.");
            }
        
            if (!data || !data.overlayed_image) {
                throw new Error("No segmented image received.");
            }
        
            // Show output and update segmented image
            outputDiv.style.display = "block";
            message.innerHTML = `<p style="color:green;">✅ ${data.message || "Segmentation successful!"}</p>`;
        
            // Display segmented image
            segmentedImage.src = data.overlayed_image;
            segmentedImage.style.display = "block";
        } catch (error) {
            console.error("Error:", error);
            message.innerHTML = `<p style="color:red;">❌ ${error.message}</p>`;
        } finally {
            // Re-enable button
            submitButton.disabled = false;
            buttonText.style.display = "inline";
            spinner.style.display = "none";
        }        
    });
});
