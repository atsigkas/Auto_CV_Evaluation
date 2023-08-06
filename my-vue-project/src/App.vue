<template>
  <div>
    <header>
      <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap" rel="stylesheet">
      <h1>
        <span class="blue">ev</span>
        <span class="bluegreen">AI</span>
        <span class="blue">.luator</span>
      </h1>
      <h2>"Artificially Transparent CV Evaluation"</h2>
    </header>
    <main>
      <div class="job-container">
        <div class="job-title-container">
          <label for="job-title">Job Title</label>
          <textarea id="job-title" v-model="jobTitle" class="job-title-textarea"></textarea>
        </div>
        <div class="job-description-container">
          <label for="job-description">Job Description</label>
          <textarea id="job-description" v-model="jobDescription" class="job-description-textarea"></textarea>
        </div>
      </div>
    </main>
    <div class="buttons-container" style="display: flex; gap: 20px;">
      <div class="upload-button-container">
        <input type="file" @change="handleFileChange" accept=".pdf" multiple style="display: none;" ref="fileInput" />
        <button class="upload-button" @click="openFileInput">
          <svg
            xmlns="http://www.w3.org/2000/svg" 
            height="0.5em" 
            viewBox="0 0 512 512"
            fill="rgba(234, 182, 118, 0.8)">
            <path d="M288 109.3V352c0 17.7-14.3 32-32 32s-32-14.3-32-32V109.3l-73.4 73.4c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l128-128c12.5-12.5 32.8-12.5 45.3 0l128 128c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L288 109.3zM64 352H192c0 35.3 28.7 64 64 64s64-28.7 64-64H448c35.3 0 64 28.7 64 64v32c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V416c0-35.3 28.7-64 64-64zM432 456a24 24 0 1 0 0-48 24 24 0 1 0 0 48z"/>
          </svg>
          Upload PDF
        </button>
        <button class="toggle-sidebar-button" @click="toggleSidebar">Toggle Sidebar</button>
      </div>
      <div class="submit-container"> <!-- Wrap the submit button in a container -->
        <button class="submit-button" @click="submitForm">Submit</button>
      </div>
    </div>
    <div class="file-size-info">
      Max File Size 5MB
    </div>
    <ResultPopup v-if="showPopup" :results="results" @close="closePopup" />
  </div>
  <div class="uploaded-files">
    <h3>Uploaded PDF Files:</h3>
    <ul>
      <li v-for="(file, index) in pdfFiles" :key="index">{{ file.name }}</li>
    </ul>
  </div>
  <SidebarContainer
  ref="sidebarContainer"
  v-if="showSidebar"
  :pdfFiles="pdfFiles"
  @update-pdf-files="updatePdfFiles"
  />
</template>


<script>
import ResultPopup from "./components/ResultPopup.vue";
import SidebarContainer from "./components/SidebarContainer.vue"; 

export default {
  components: {
    ResultPopup,
    SidebarContainer 
  },
  data() {
    return {
      cvText: "",
      jobTitle: "",
      jobDescription: "",
      showPopup: false, // Track whether the popup should be shown
      results: [], // Store the list of results to be shown in the popup
      pdfFiles: [],
      showSidebar: false,
    };
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const files = event.target.files;
      const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');

      // Append the new PDF files to the existing list
      this.pdfFiles = [...this.pdfFiles, ...pdfFiles];

      // Use $nextTick to ensure the DOM has been updated before accessing refs
      this.$nextTick(() => {
        if (this.$refs.sidebarContainer) {
          this.$refs.sidebarContainer.updateLocalPdfFiles(this.pdfFiles);
        }
      });
    },
    submitForm() {
      // Do any processing you need to get the list of results
      // For demonstration purposes, we'll just create a sample list of results here
      this.results = [
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
        { id: 2, text: "Result 2" },
        { id: 3, text: "Result 3" },
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
        { id: 2, text: "Result 2" },
        { id: 3, text: "Result 3" },
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
        { id: 2, text: "Result 2" },
        { id: 3, text: "Result 3" },
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
        { id: 2, text: "Result 2" },
        { id: 3, text: "Result 3" },
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
        { id: 2, text: "Result 2" },
        { id: 3, text: "Result 3" },
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
        { id: 2, text: "Result 2" },
        { id: 3, text: "Result 3" },
        { id: 1, text: "Result 1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" },
      ];

      // Show the popup
      this.showPopup = true;
    },
    closePopup() {
      // Close the popup when the user clicks the "Close" button
      this.showPopup = false;
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    updatePdfFiles(pdfFiles) {
    this.pdfFiles = pdfFiles;
    },
  }
};
</script>

<style>
/* Define a default background image for larger screens */
body {
  background-image: url('~@/assets/bck_image/neuro.jpg');
  background-size: calc(100vw + 100px) calc(100vh + 100px);
  background-repeat: no-repeat;
}

/* Use a media query to adjust the background image for smaller screens */
@media (max-width: 768px) {
  body {
    background-image: url('~@/assets/bck_image/neuro.jpg');
    background-size: calc(100vw + 100px) calc(100vh + 100px);
    background-repeat: no-repeat;
  }
}

header {
  background-color: rgba(0, 0, 0, 0.7); /* Slightly transparent background color for the header */
  padding: 20px;
  max-width: 600px; /* Set the maximum width for the main section */
  margin-left: auto; /* Center the main section */
  margin-right: auto; /* Center the main section */
  text-align: center;
  border-radius: 10px; /* Add rounded corners with a value that suits your design */
}

h1 {
  font-size: 24px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
}

.blue {
  color: #0fe2f7; /* Update the color of the blue letters */
}

.bluegreen {
  color: rgba(234, 182, 118, 0.8);
}

h2 {
  color: rgba(234, 182, 118, 0.8); /* Slightly transparent color for the h2 element */
  font-size: 18px;
  margin-top: 10px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
}

main {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  background-color: rgba(4, 73, 109, 0.1);
  padding: 20px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  border-radius: 10px; /* Add rounded corners to the main section as well */
}

.uploaded-files {
  margin-top: 20px;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 10px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.uploaded-files h3 {
  color: rgba(234, 182, 118, 0.8);
  font-size: 18px;
}

.uploaded-files ul {
  list-style: none;
  padding: 0;
  margin-top: 10px;
}

.uploaded-files li {
  color: white;
  margin-bottom: 5px;
}

.toggle-sidebar-button {
  margin-bottom: 5px;
  background-color: transparent;
  color: white;
  padding: 10px 20px;
  border: 2px solid rgba(234, 182, 118, 0.8);
  border-radius: 20px; /* Increase the border radius for rounded corners */
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-sidebar-button:hover {
  background-color: rgba(234, 182, 118, 0.4);
}

.job-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.job-title-container {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.job-title-textarea {
  height: 20px; /* Set the desired height for the job title textarea */
  width: 500px;
  resize: none;
}

.job-description-container {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
}

.job-description-textarea {
  height: 150px; /* Set the desired height for the text areas */
  width: 500px;
  resize: none; /* Set the desired height for the job description textarea */
}

label {
  border-radius: 5px 0 0 0;
  padding: 5px 10px;
  color: white;
  margin-bottom: 5px;
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
}

textarea {
  width: 300px;
  height: 50px;
  border: 1px solid rgba(234, 182, 118, 0.5);
  padding: 5px;
  border-radius: 10px; /* Set the same border-radius for all four corners */
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  font-family: 'Montserrat', sans-serif;
}

.buttons-container {
  margin-top: 20px;
  display: flex;
  justify-content: center; /* Center the buttons horizontally */
}

.upload-button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-button {
  margin-bottom: 5px;
  background-color: transparent;
  color: white;
  padding: 10px 20px;
  border: 2px solid rgba(234, 182, 118, 0.8);
  border-radius: 20px; /* Increase the border radius for rounded corners */
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button svg {
  width: 20px;
  height: 20px;
  fill: white; /* Set the color of the SVG image to white */
}

/* Add the glowing effect for the button when hovering */
.upload-button::after {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.5s ease-out;
  pointer-events: none; /* Ensure the glowing effect doesn't interfere with the button click */
}

.upload-button:hover::after {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

/* Add the glowing effect for the button borders when hovering */
.upload-button::before {
  content: "";
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100%;
  border: 2px solid rgba(234, 182, 118, 0.8);
  border-radius: 5px;
  opacity: 0;
  animation: glow-border 1.5s linear infinite;
  pointer-events: none; /* Ensure the glowing effect doesn't interfere with the button click */
}

.upload-button:hover::before {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

.submit-container {
  position: relative;
  overflow: hidden;
  display: inline-block;
  border-radius: 100px; /* Increase the border radius to make it round */
  padding: 5px; /* Adjust the padding to change the size */
  display: flex;
  align-items: center;
}

.submit-button {
  background-color: rgba(234, 182, 118, 0.2);
  color: white;
  padding: 10px 20px;
  font-size: 14px; /* Adjust the font size to match the upload button */
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  white-space: nowrap; /* Prevent text from wrapping */
  border: none;
  border-radius: 20px; /* Keep the border radius for the button */
  font-family: 'Montserrat', sans-serif;
  font-weight: bold;
  height: 40px;
  width: 150px;
  transition: background-color 0.3s ease-out;
}

.submit-button:hover {
  background-color: rgba(234, 182, 118, 0.4); /* Change to a brighter background color on hover */
}

/* Adjust the glowing effect for the button and container when hovering */
.submit-button::after {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(234, 182, 118, 0.1);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.5s ease-out;
  pointer-events: none;
  animation: glowing-border 2s linear infinite;
}

/* Adjust the glowing effect for the submit button when hovering */
.submit-button:hover::after {
  opacity: 1;
}

/* Add the glowing effect for the submit button borders when hovering */
.submit-button::before {
  content: "";
  position: absolute;
  bottom: -5px; /* Adjust the glowing effect position for the lower border */
  right: -5px;
  width: calc(100% + 10px); /* Extend the glowing effect outside the button */
  height: calc(100% + 10px);
  border: 2px solid rgba(234, 182, 118, 0.8);
  border-radius: 20px; /* Increase the border radius to make it round */
  opacity: 0;
  animation: glow-border 1.5s linear infinite;
  pointer-events: none;
}

/* Adjust the glowing effect for the submit button borders when hovering */
.submit-container {
  position: relative;
  overflow: hidden;
  display: inline-block;
  border-radius: 100px; /* Increase the border radius to make it round */
  padding: 5px; /* Adjust the padding to change the size */
  display: flex;
  align-items: center;
}

.submit-container::before {
  content: "";
  position: absolute;
  top: -5px;
  left: -5px;
  width: calc(100% + 10px);
  height: calc(100% + 10px);
  border: 2px solid rgba(234, 182, 118, 0.8); /* Apply the glowing effect to the borders */
  border-radius: 100px; /* Increase the border radius to make it round */
  opacity: 0;
  animation: glowing-border 1.5s linear infinite;
  pointer-events: none;
}

/* Adjust the glowing effect for the submit button container borders when hovering */
.submit-container:hover::before {
  opacity: 1;
}

@keyframes glowing-border {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.6;
  }
  100% {
    transform: scale(1);
    opacity: 0.8;
  }
}

@keyframes glow-border {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.6;
  }
  100% {
    transform: scale(1);
    opacity: 0.8;
  }
}

.upload-info {
  color: rgba(234, 182, 118, 0.8);
  font-size: 14px;
  margin-top: 5px;
}

.file-size-info {
  color: rgba(234, 182, 118, 0.3); /* Set the desired color for the text */
  font-size: 13px; /* Set the desired font size for the text */
  text-align: center; /* Center the text horizontally */
  margin-top: 10px; /* Add some top margin to separate it from the buttons */
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
  margin-left: -210px; /* Add left margin to move it a bit to the left */
  margin-top: -1px; 
}
</style>
