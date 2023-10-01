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
              <div class="pdf-count-container">
                <div class="pdf-icon">
                  <img src="@/assets/pdf-image.svg" alt="PDF Icon" class="pdf-icon" />
                </div>
                <span class="pdf-count">{{ localPdfFiles.length }}</span>
              </div>
            </div>
            <div class="pdf-container">
              <ul class="uploaded-pdf-list">
                <li v-for="(file, index) in localPdfFiles" :key="index" class="pdf-list-item">
                  <button @click="showWarning(index)" class="remove-button"
                    :class="{ glowing: showConfirmation && removeIndex === index }">
                    <div class="remove-icon">
                      <svg fill="#000000" height="30px" width="30px" version="1.1" id="Layer_1"
                        viewBox="-51.2 -51.2 614.40 614.40" stroke="#000000" stroke-width="0.00512">
                        <g id="SVGRepo_bgCarrier" stroke-width="0" />
                        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
                        <g id="SVGRepo_iconCarrier">
                          <g>
                            <g>
                              <path
                                d="M60.236,210.824L90.354,512h331.294l30.118-301.176H60.236z M188.236,459.294H143.06V263.529h45.176V459.294z M278.589,459.294h-45.177V263.529h45.177V459.294z M368.942,459.294h-45.176V263.529h45.176V459.294z" />
                            </g>
                          </g>
                          <g>
                            <g>
                              <path
                                d="M391.53,90.353h-52.706v-7.529C338.824,37.155,301.67,0,256.001,0s-82.824,37.155-82.824,82.824v7.529h-52.706 c-44.767,0-81.908,32.565-89.08,75.294h449.218C473.438,122.918,436.297,90.353,391.53,90.353z M293.648,90.353h-75.294v-7.529 c0-20.759,16.888-37.647,37.647-37.647s37.647,16.888,37.647,37.647V90.353z" />
                            </g>
                          </g>
                        </g>
                      </svg>
                    </div>
                  </button>
                  <span>{{ file.name }}</span>
                </li>
              </ul>
            </div>
          </div>
          <CandidatesTable :candidates="candidates" :jobTitle='jobTitle' :jobDescription='jobDescription' :ranking="ranking" @updateRanking="updateRanking" />
          <RankingCandidates :ranking="ranking" />
        </div>
      </div>
    </div>
    <div v-if="showConfirmation" class="confirmation-message">
      <p>Remove file permanently?</p>
      <div class="confirmation-buttons">
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
    jobTitle: {
      type: String
    },
    jobDescription: {
      type: String
    }
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
        this.animateRemoved = false;
        this.animateRemove = false;
        this.localPdfFiles.splice(index, 1);
        this.updatePdfFiles();
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
      this.$store.dispatch('setFunctionName', '');
    },
    candidateEditUrl({ id }) {
      const inputRow = document.getElementById(id)
      inputRow.classList.toggle('active')
    },
    // call backend endpoint and on finish close the url input
    saveUrl({ id }) {
      const inputRow = document.getElementById(id)
      inputRow.classList.remove('active')
    },
    // show the publivations
    publicationEdit() {
      this.showPublications = true
    },
    candidateForm(event) {
      event.preventDefault()
    }
  },
};
</script>

<style src="./SidebarContainer.css">
/* LIST */
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

