<template>
  <div class="sidebar-container" ref="sidebarContainer">
    <div :class="sidebarClass">
      <div class="tabs-wrapper">
        <div class="tab-actions">
          <div class="tab-item active" id="pdf-tab">
            <h2 role="button" @click="tabSelector({ id: 'pdf-tab' })" class="tab-title">PDF Documents</h2>
          </div>
          <div class="tab-item" id="candidates-tab">
            <h2 role='button' @click="tabSelector({ id: 'candidates-tab' })" class="tab-title">Candidates</h2>
          </div>
          <div class="tab-item" id="ranking-tab">
            <h2 role='button' @click="tabSelector({ id: 'ranking-tab' })" class="tab-title">Ranking</h2>
          </div>
        </div>
        <div class="tab-content-wrapper">
          <div class="tab-content active" id="pdf-tab-content">
            <div class="pdf-icon-container">
              <div class="file-count-container">
                <div class="pdf-icon"
                  :class="{ 'green-icon': greenIcon, 'animate-removed': animateRemoved, 'animate-remove': animateRemove }">
                  <img src="@/assets/pdf-image.svg" alt="PDF Icon" class="pdf-icon"
                    :class="{ 'green-icon': greenIcon, pdfIcon: true, 'animate-removed': animateRemoved, 'animate-remove': animateRemove }" />
                </div>
                <span class="file-count">{{ localPdfFiles.length }}</span>
              </div>
            </div>
            <div class="files-container">
              <ul class="uploaded-files-list">
                <li v-for="(file, index) in localPdfFiles" :key="index" class="file-list-item">
                  <button @click="showWarning(index)" class="remove-button"
                    :class="{ glowing: showConfirmation && removeIndex === index }">
                    <img src="@/assets/remove-svgrepo-com.svg" alt="Remove" class="remove-icon" />
                  </button>
                  <span>{{ file.name }}</span>
                </li>
              </ul>
            </div>
          </div>
          <CandidatesTable :candidates="candidates" :jobTitle='jobTitle' :jobDescription='jobDescription' :ranking="ranking" @updateRanking="updateRanking"/>
          <RankingCandidates :results="results" :ranking="ranking" />
        </div>
      </div>
    </div>
    <div v-if="showConfirmation" class="confirmation-message">
      <p>Remove file permanently?</p>
      <div class="confirmation-divttons">
        <button @click="confirmRemove" class="confirm-button">Yes</button>
        <button @click="cancelRemove" class="cancel-button">No</button>
      </div>
      <label>
        <input type="checkbox" v-model="dontShowAgain" @change="updateLocalStorage" />
        Don't show this message again
      </label>
    </div>
  </div>
</template>

<script>
import RankingCandidates from "./RankingCandidates.vue";
import CandidatesTable from "./CandidatesTable.vue";

export default {
  components: {
    CandidatesTable,
    RankingCandidates
  },
  props: {
    pdfFiles: {
      type: Array,
      required: true,
    },
    candidates: {
      type: Array,
      required: true,
    },
    results: {
      type: Array,
      required: true,
    },
    jobTitle:{
      type: String
    },
    jobDescription:{
      type: String
    },
    greenIcon: Boolean, 
  },
  data() {
    return {
      localPdfFiles: [...this.pdfFiles],
      showConfirmation: false,
      dontShowAgain: false,
      removeIndex: null,
      showSidebar: false,
      animateRemove: false,
      ranking: []
    };
  },
  computed: {
    pdfIconClass() {
      const iconColor = this.localPdfFiles.length > this.pdfFiles.length ? 'green' : 'red';
      return `pdf-icon ${iconColor}-icon`;
    },
    sidebarClass() {
      return {
        sidebar: true,
        hidden: !this.showSidebar, 
      };
    },
  },
  mounted() { 
    this.dontShowAgain = false;
    this.showConfirmation = false; 
    this.showPublications - false;
    console.log('dontShowAgain:', this.dontShowAgain);

    document.addEventListener('click', this.handleOutsideClick);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleOutsideClick);
  },
  methods: {
    updateRanking(newData) {
      this.ranking = newData;
    },
    removeFile(index) {
      if (index !== null && index < this.localPdfFiles.length) {
        this.animateRemoved = true;
        this.animateRemove = true; 

        setTimeout(() => {
          this.animateRemoved = false;
          this.animateRemove = false; 
          this.localPdfFiles.splice(index, 1);
          this.updatePdfFiles();
        }, 2000); 
      }
    },
    updateLocalPdfFiles(pdfFiles) {
      this.localPdfFiles = pdfFiles;
      this.updatePdfFiles();
    },
    showWarning(index) {
      if (this.dontShowAgain) {
        this.removeFile(index);
      } else {
        this.showSidebar = true;
        this.showConfirmation = true;
        this.removeIndex = index;
      }
    },
    updateLocalStorage() {
      localStorage.setItem('dontShowAgain', this.dontShowAgain.toString());
      console.log('localStorage updated:', this.dontShowAgain);

      if (this.dontShowAgain) {
        this.$emit('update-pdf-files', this.localPdfFiles);
        this.showConfirmation = false; // Simply hide the confirmation box
      }
    },
    confirmRemove() {
      this.removeFile(this.removeIndex); // Call the removeFile method directly
      this.showConfirmation = false;
      this.removeIndex = null;
    },
    updatePdfFiles() {
      this.$emit('update-pdf-files', this.localPdfFiles);
    },
    cancelRemove() {
      this.showConfirmation = false;
      this.removeIndex = null;
    },
    handleOutsideClick(event) {
      // Check if the clicked element is outside the sidebar container
      const sidebarContainer = this.$refs.sidebarContainer;
      if (!sidebarContainer.contains(event.target)) {
        this.showSidebar = false;
        this.showConfirmation = false;
        this.removeIndex = null;
      }
    },
    tabSelector({ id }) {
      const tabItems = document.querySelectorAll('.tab-item')
      const tabContents = document.querySelectorAll('.tab-content')
      const tabItem = document.getElementById(id)
      const tabContent = document.getElementById(`${id}-content`)
      console.log(`${id}-content`)

      tabItems.forEach(item => {
        item.classList.remove('active')
      })
      tabContents.forEach(content => {
        content.classList.remove('active')
      }
      )
      tabItem.classList.add('active')
      tabContent.classList.add('active')
    },
    candidateEditUrl({ id }) {
      const inputRow = document.getElementById(id)
      inputRow.classList.toggle('active')
    },
    saveUrl({ id }) {
      // call backend endpoint and on finish close the url input
      const inputRow = document.getElementById(id)
      inputRow.classList.remove('active')
    },
    publicationEdit() {
      this.showPublications = true
    },
    closeDialog() {
      this.showPublications = false
    },
    candidateForm(event) {
      event.preventDefault()
      //write some code
    }
  },
};
</script>

<style scoped>
.sidebar-container {
  display: flex;
  align-items: flex-start;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0px;
  /* Initially hide the sidebar */
  width: 100%;
  /* Adjust the width to make the sidebar wider */
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
  transition: left 0.3s ease-in-out;
  z-index: 10;
  padding-top: 100px;
}

.sidebar.active {
  left: 0;
}

.sidebar h3 {
  font-size: 20px;
  color: rgba(234, 182, 118, 0.8);
  margin: auto;
  padding-bottom: 5%;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold;
}

.pdf-icon-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: auto;
}

.file-count-container {
  display: flex;
  align-items: center;
  margin-bottom: 4%;
}

.file-count {
  color: rgba(15, 226, 247, 0.6);
  font-weight: bold;
  font-size: 30px;
  font-family: 'Montserrat', sans-serif;
  margin-left: 8px;
  padding-left: 1%;
}

.pdf-icon {
  content: url('~@/assets/pdf-image.svg');
  filter: invert(100%);
  width: 30px;
  height: 30px;
  padding-right: 1%;
}

.sidebar.hidden {
  left: -13px;
}

.files-container {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  overflow: auto;
}

.uploaded-files-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.uploaded-files-list li {
  color: white;
  padding-bottom: 4%;
  border-bottom: 1px solid rgba(15, 226, 247, 0.6);
  text-align: center;
}

.uploaded-files-list li:last-child {
  border-bottom: none;
  padding-bottom: 8%;
}

.uploaded-files-list li {
  word-wrap: break-word;
  white-space: normal;
}

.file-list-item {
  color: white;
  margin-bottom: 5px;
  padding-bottom: 2px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  /* Add a border between list items */
  text-align: center;
  /* Align the text to the center */
  /* Apply word wrapping to the list items */
  word-wrap: break-word;
  white-space: normal;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold;
  /* Make the text bold */
}

.remove-button {
  border: 0;
  border-radius: 50%;
  padding: 0;
  cursor: pointer;
  margin-left: 94%;
  margin-top: 1%;
  display: flex;
  width: 5%;
  height: 5%;
  transition: background-color 0.4s ease-in-out;
  background: transparent
}

.remove-icon {
  width: 100%;
  height: 100%;
  filter: invert(100%);
  padding-left: 15%;
}


.confirmation-message {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 250px;
  transform: translate(-50%, -50%);
  max-height: calc(100% - 40px);
  overflow-y: auto;
  background-color: rgba(0, 0, 0, 0.9);
  border-radius: 5px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 999;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.9);
  border: 2px solid rgba(234, 182, 118, 0.8);
  border-top: 2px solid rgba(234, 182, 118, 0.8);
}

.confirmation-message p {
  color: #0fe2f7;
  font-size: 14px;
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
}

.confirmation-message label {
  color: white;
  font-size: 12px;
  font-family: 'Montserrat', sans-serif;
}

.confirmation-buttons {
  display: flex;
  margin-top: 5px;
  margin-bottom: 5px;
}

.confirm-button,
.cancel-button {
  margin-top: 0;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold;
}

.confirm-button {
  background-color: rgba(234, 182, 118, 0.8);
  color: white;
  margin-right: 5px;
}

.cancel-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.confirmation-message input[type="checkbox"] {
  margin-right: 5px;
  vertical-align: middle;
}

.animate-remove {
  animation: colorChange 2s;
  transition: filter 3s ease-in-out;
}

.tabs-wrapper {
  max-width: 900px;
  width: 100%;
}

.tab-actions {
  display: flex;
  margin-left: -5px;
  margin-top: -5px;
  justify-content: space-evenly;
  margin-bottom: 20px;
}

.tab-item {
  margin-left: 5px;
  margin-top: 5px;
}

.tab-item .tab-title {
  font-size: 18px;
  line-height: 1.2;
  display: block;
  font-weight: 700;
  cursor: pointer;

}

.tab-item .tab-title:hover {
  opacity: 0.8;
  transition: all 0.3s ease;
}

.tab-item.active .tab-title {
  border-bottom: 1px solid rgba(234, 182, 118, 0.8);
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}


.list {
  flex: 0 0 50%;
  max-width: 50%;
  padding: 20px;
  margin: -10px 0 0;

}

.list li {
  margin-top: 10px;
  line-height: 22px;
}

.list-head {
  margin-bottom: 20px
}

.list-head h3 {
  padding: 0;
  margin: 0;
}

</style>
