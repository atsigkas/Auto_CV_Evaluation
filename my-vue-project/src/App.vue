<template>
  <div>
    <header>
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
          <label for="job-title">Job Title:</label>
          <textarea id="job-title" v-model="jobTitle" class="job-title-textarea"></textarea>
        </div>
        <div class="job-description-container">
          <label for="job-description">Job Description:</label>
          <textarea id="job-description" v-model="jobDescription" class="job-description-textarea"></textarea>
        </div>
      </div>
    </main>
    <div class="buttons-container">
      <div class="upload-button-container">
        <input type="file" @change="handleFileChange" accept=".pdf" style="display: none;" ref="fileInput" />
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
        <p class="upload-info">Maximum file size: 5MB</p>
      </div>
      <button class="submit-button" @click="submitForm">Submit</button>
    </div>
    <ResultPopup v-if="showPopup" :results="results" @close="closePopup" />
  </div>
</template>

<script>
import ResultPopup from "./ResultPopup.vue";

export default {
  components: {
    ResultPopup,
  },
  data() {
    return {
      cvText: "",
      jobTitle: "",
      jobDescription: "",
      showPopup: false, // Track whether the popup should be shown
      results: [], // Store the list of results to be shown in the popup
    };
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      // Do something with the selected file (e.g., store it in a variable or upload it)
      console.log("Selected file:", file);
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
}


.job-description-container {
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
}

.job-description-textarea {
  height: 100px; /* Set the desired height for the job description textarea */
}


label {
  border-radius: 5px 0 0 0;
  padding: 5px 10px;
  color: white;
  margin-bottom: 5px;
}

textarea {
  width: 300px;
  height: 50px;
  border: 2px solid rgba(234, 182, 118, 0.5);
  padding: 5px;
  border-radius: 0 5px 5px 5px;
  background-color: rgba(0, 0, 0, 0.7); /* Transparent background color for the textarea */
  color: white; /* Set the text color to white */
}

.buttons-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-button {
  margin-bottom: 5px;
  background-color: #333;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  position: relative; /* Add a position property to the button */
  overflow: hidden; /* Hide the glowing effect outside the button */
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-button svg {
  width: 20px;
  height: 20px;
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
  top: 0;
  left: 0;
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

.submit-button {
  background-color: #333;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  position: relative; /* Add a position property to the button */
  overflow: hidden; /* Hide the glowing effect outside the button */
}

/* Add the glowing effect for the button when hovering */
.submit-button::after {
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

.submit-button:hover::after {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

/* Add the glowing effect for the button borders when hovering */
.submit-button::before {
  content: "";
  position: absolute;
  bottom: 0; /* Adjust the glowing effect position for the lower border */
  right: 0;
  width: 100%;
  height: 100%;
  border: 2px solid rgba(234, 182, 118, 0.8);
  border-radius: 5px;
  opacity: 0;
  animation: glow-border 1.5s linear infinite;
  pointer-events: none; /* Ensure the glowing effect doesn't interfere with the button click */
}

.submit-button:hover::before {
  opacity: 1; /* Make the glowing effect visible when hovering */
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
</style>
