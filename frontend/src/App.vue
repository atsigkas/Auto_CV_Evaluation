<template>
  <div>
    <header>
      <div class="hamburger-wrap">
        <button class="hamburger" type="button" @click="toggleSidebar">
          <span class="hamburger__line"></span>
          <span class="hamburger__middle"></span>
          <span class="icon-bar hamburger__line"></span>
        </button>
      </div>
      <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap" rel="stylesheet">
      <h1>
        <span class="letters-color-blue">ev</span>
        <span class="letters-color-gold">AI</span>
        <span class="letters-color-blue">.luator</span>
      </h1>
      <h2>"Artificially Transparent CV Evaluation"</h2>
    </header>
    <main>
      <div class="job-container">
        <div class="job-title-container">
          <label for="job-title">Academic Position Title</label>
          <input id="job-title" v-model="positionTitle" class="job-title-textarea" />
        </div>
        <div class="job-description-container">
          <label for="job-description">Academic Position Description</label>
          <textarea id="job-description" v-model="positionDescription" class="job-description-textarea"></textarea>
        </div>
      </div>
    </main>
    <div class="buttons-container" style="display: flex; gap: 20px;">
      <div class="upload-button-container">
        <input type="file" @change="handleFileChange" accept=".pdf" multiple style="display: none;" ref="fileInput" />
        <button class="upload-button" @click="openFileInput">
          <svg xmlns="http://www.w3.org/2000/svg" height="0.5em" viewBox="0 0 512 512" fill="rgba(234, 182, 118, 0.8)">
            <path
              d="M288 109.3V352c0 17.7-14.3 32-32 32s-32-14.3-32-32V109.3l-73.4 73.4c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3l128-128c12.5-12.5 32.8-12.5 45.3 0l128 128c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L288 109.3zM64 352H192c0 35.3 28.7 64 64 64s64-28.7 64-64H448c35.3 0 64 28.7 64 64v32c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V416c0-35.3 28.7-64 64-64zM432 456a24 24 0 1 0 0-48 24 24 0 1 0 0 48z" />
          </svg>
          Upload PDF
        </button>
        <div class="file-size-info">
      Max File Size 5MB
    </div>
      </div>
      <div class="submit-container"> <!-- Wrap the submit button in a container -->
        <button class="submit-button" :disabled="isButtonDisabled" @click="submitForm">Submit</button>
      </div>
    </div>
  </div>
  <SidebarContainer ref="sidebarContainer" v-if="showSidebar" :pdfFiles="pdfFiles" :candidates="candidates" :positionTitle='positionTitle' :positionDescription='positionDescription'
    @update-pdf-files="updatePdfFiles" />
  <SpinnerLoading />
  <DialogComponent />
</template>


<script>
import axios from 'axios';
import SidebarContainer from "./components/SidebarContainer.vue";
import SpinnerLoading from "./components/Spinnerloading.vue";
import DialogComponent from "./components/DialogComponent.vue";

export default {
  components: {
    SidebarContainer,
    SpinnerLoading,
    DialogComponent
  },
  data() {
    return {
      positionTitle: "",
      positionDescription: "",
      candidates:[],
      pdfFiles: [],
      showSidebar: false
    }
  },
  computed: {
    isButtonDisabled() {
      const disabled = !this.pdfFiles || this.pdfFiles.length === 0 || !this.positionTitle || !this.positionDescription;
      console.log('Button Disabled:', disabled);  // Log the value
      return disabled;
    },
    functionName() {
      return this.$store.state.functionName;
    }
  },
  watch: {
    functionName(newVal) {
      if (newVal && typeof this[newVal] === 'function') {
        this[newVal]();
      }
    }
  },
  methods: {
    showDialog(text) {
      this.$store.dispatch('showDialog', text);
    },
    showSpinner(text) {
      this.$store.dispatch('showSpinner', text);
    },
    hideSpinner(){
      this.$store.dispatch('hideSpinner');
    },
    closeErrorPopup() {
      this.showErrorPopup = false;
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const files = event.target.files;
      const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');

      if (pdfFiles.length > 0) {
        this.pdfFiles = [...this.pdfFiles, ...pdfFiles];
        this.$nextTick(() => {
          if (this.$refs.sidebarContainer) {
            this.$refs.sidebarContainer.updateLocalPdfFiles(this.pdfFiles);
          }
        });
        this.showDialog("Pdf are uploaded.")
      }
      event.target.value = null;
    },

    uploadFiles() {
      this.showSpinner("Waiting to find the Candidates.It will take some time.")
      const formData = new FormData();

      // Add each file to the FormData object
      for (let i = 0; i < this.pdfFiles.length; i++) {
        formData.append('files', this.pdfFiles[i]);
      }

      // Add the two string values
      formData.append('positionTitle', this.positionTitle);
      formData.append('positionDescription', this.positionDescription);
      
      
      axios.post('http://127.0.0.1:8000/api-endpoint/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          this.hideSpinner()
          if (!response.data.candidates) {
            this.showDialog("Something went wrong.")
          } else {
            this.candidates = response.data.candidates;
            this.showDialog("We found the candidates.")
          }
        })
        .catch(error => {
          this.hideSpinner();
          this.showDialog("We had an unexpected error:"+ error.response.data.message);
        });
      this.pdfFiles=[];
    }
    ,
    submitForm() {
      this.uploadFiles()
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
      this.$store.dispatch('setFunctionName', '');
    },
    updatePdfFiles(pdfFiles) {
      this.pdfFiles = pdfFiles;
    },
  }
};
</script>

<style src="./styles.css"></style>

