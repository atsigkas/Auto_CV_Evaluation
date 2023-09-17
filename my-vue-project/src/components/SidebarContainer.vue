<template>
  <div class="sidebar-container" ref="sidebarContainer">
    <div :class="sidebarClass">
      <div class="pdf-icon-container">
        <h3 >Uploaded Files</h3>
        //TODO: remove after
  <Candidates/>

        <div class="file-count-container">
          <div class="pdf-icon" :class="{ 'green-icon': greenIcon, 'animate-removed': animateRemoved, 'animate-remove': animateRemove }">
            <img
              src="@/assets/pdf-image.svg"
              alt="PDF Icon"
              class="pdf-icon"
              :class="{ 'green-icon': greenIcon, pdfIcon: true, 'animate-removed': animateRemoved, 'animate-remove': animateRemove }"
            />
          </div>
          <span class="file-count">{{ localPdfFiles.length }}</span>
        </div>
      </div>
      <div class="files-container">
        <ul class="uploaded-files-list">
          <li v-for="(file, index) in localPdfFiles" :key="index" class="file-list-item">
            <button
              @click="showWarning(index)"
              class="remove-button"
              :class="{ glowing: showConfirmation && removeIndex === index }"
            >
              <img src="@/assets/remove-svgrepo-com.svg" alt="Remove" class="remove-icon" />
            </button>
            <span>{{ file.name }}</span>
          </li>
        </ul>
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
import Candidates from "./Candidates.vue";

export default {
  components: {
    Candidates
  },
  props: {
    pdfFiles: {
      type: Array,
      required: true,
    },
    greenIcon: Boolean, // Add this line
  },
  data() {
    return {
      localPdfFiles: [...this.pdfFiles],
      showConfirmation: false,
      dontShowAgain: false,
      removeIndex: null,
      showSidebar: false,
      animateRemove: false,
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
        hidden: !this.showSidebar, // Add the hidden class when showSidebar is false
      };
    },
  },
  mounted() { // Use mounted instead of created
    // Set dontShowAgain to false when the component is mounted
    this.dontShowAgain = false;
    this.showConfirmation = false; // Ensure that showConfirmation is set to false
    // Check if there is a value in localStorage and update dontShowAgain accordingly
    console.log('dontShowAgain:', this.dontShowAgain);

    // Event listener to close sidebar and confirmation messages when clicking outside
    document.addEventListener('click', this.handleOutsideClick);
  },
  beforeUnmount() {
    // Remove the event listener when the component is destroyed
    document.removeEventListener('click', this.handleOutsideClick);
  },
  methods: {
    removeFile(index) {
      if (index !== null && index < this.localPdfFiles.length) {
        // Trigger the animation
        this.animateRemoved = true;
        this.animateRemove = true; // Set animateRemove to true

        // Use setTimeout to reset the animation after a delay
        setTimeout(() => {
          this.animateRemoved = false;
          this.animateRemove = false; // Set animateRemove to true
          // Remove the file from the list
          this.localPdfFiles.splice(index, 1);
          this.updatePdfFiles();
        }, 2000); // Set the delay to 2000ms (2 seconds)
      }
    },
    // Method to update the localPdfFiles array
    updateLocalPdfFiles(pdfFiles) {
      this.localPdfFiles = pdfFiles;
      this.updatePdfFiles();
    },
    showWarning(index) {
      if (this.dontShowAgain) {
        this.removeFile(index); // Call the removeFile method directly
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
  },
};
</script>

<style scoped>
.sidebar-container {
  display: flex;
  align-items: flex-start; /* Align items to the top */
}
.sidebar {
  position: fixed;
  top: 0;
  left:0px; /* Initially hide the sidebar */
  width: 25%; /* Adjust the width to make the sidebar wider */
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center; /* Align items horizontally to the center */
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
  transition: left 0.3s ease-in-out; /* Add the transition back */
  z-index: 10;
  padding-top: 100px;
}

.sidebar.active {
  left: 0; /* Adjust the left position to fully display the sidebar */
}

.sidebar h3 {
  font-size: 20px;
  color: rgba(234, 182, 118, 0.8);
  margin: auto;
  padding-bottom: 5%;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
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
  content: url('~@/assets/pdf-image.svg'); /* Replace with the actual path to your white PDF icon */
  filter: invert(100%);
  width: 30px;
  height: 30px;
  padding-right: 1%;
}

.sidebar.hidden {
  left: -13px; /* Move the sidebar out of view */
}

.files-container {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Align items to the top */
  align-items: stretch; /* Stretch items horizontally */
  overflow: auto; /* Add scrollbars if the list is too long */
}

.uploaded-files-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.uploaded-files-list li {
  color: white;
  padding-bottom: 4%; /* Add padding for better readability */
  border-bottom:1px solid rgba(15, 226, 247, 0.6); /* Add a border between list items */
  text-align: center; /* Align the text to the center */
}

.uploaded-files-list li:last-child {
  border-bottom: none; /* Remove border for the last list item */
  padding-bottom: 8%; /* Add padding for better readability */
}

/* Apply word wrapping to the list items */
.uploaded-files-list li {
  word-wrap: break-word;
  white-space: normal;
}

.file-list-item {
  color: white;
  margin-bottom: 5px;
  padding-bottom: 2px; /* Add padding for better readability */
  border-bottom: 2px solid rgba(255, 255, 255, 0.1); /* Add a border between list items */
  text-align: center; /* Align the text to the center */
  /* Apply word wrapping to the list items */
  word-wrap: break-word;
  white-space: normal;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
}

.remove-button {
  background-color: rgba(234, 182, 118, 0.2);
  border: 2px solid rgba(234, 182, 118, 1);
  border-radius: 50%;
  padding: 0;
  cursor: pointer;
  margin-left: 94%;
  margin-top: 1%;
  display: flex;
  width: 5%; /* Set the width of the button */
  height: 5%; /* Set the height of the button */
  transition: background-color 0.4s ease-in-out; /* Add a smooth transition for the background color */
}

.remove-icon {
  width: 100%; /* Make the image fill the available space */
  height: 100%; /* Make the image fill the available space */
  filter: invert(100%); /* Change the color of the image to white */
  padding-left: 15%;
}
.remove-button:hover {
  background-color: rgba(234, 182, 118, 0.7); /* Darken the color on hover */
}

.confirmation-message {
  position: fixed;
  top: 12%; /* Vertically center the confirmation box */
  left: calc(25% + 40px); /* Position it next to the sidebar */
  width: 250px; /* Set the desired width for the confirmation box */
  max-height: calc(100% - 40px); /* Limit the max height to the viewport - padding */
  overflow-y: auto; /* Add vertical scrollbar if content exceeds max height */
  background-color: rgba(0, 0, 0, 0.9); /* Match the background color of the sidebar */
  border-radius: 5px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 999; /* Ensure the confirmation box is above other content */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.9);
  transform: translateY(-50%); /* Adjust to vertically center the box */
  border:2px solid rgba(234, 182, 118, 0.8);
  border-top:2px solid rgba(234, 182, 118, 0.8);
}

.confirmation-message p {
  color: #0fe2f7; /* Match the text color of the sidebar header */
  font-size: 14px; /* Adjust the font size as needed */
  font-family: 'Montserrat', sans-serif;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center; /* Align the text in the center */
}

.confirmation-message label {
  color: white;
  font-size: 12px; /* Adjust the font size as needed */
  font-family: 'Montserrat', sans-serif;
}

.confirmation-buttons {
  display: flex;
  margin-top: 5px; /* Increase the margin for better separation */
  margin-bottom: 5px;
}

.confirm-button,
.cancel-button {
  margin-top: 0; /* Reset the margin-top for buttons */
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

/* Additional styling for the checkbox */
.confirmation-message input[type="checkbox"] {
  margin-right: 5px;
  vertical-align: middle;
}

.glowing {
  animation: glowing-animation 3s infinite alternate;
}

@keyframes glowing-animation {
  0% {
    box-shadow: 0 0 5px rgba(15, 226, 247, 0.1);
  }
  20% {
    box-shadow: 0 0 15px rgba(15, 226, 247, 0.3);
  }
  40% {
    box-shadow: 0 0 15px rgba(15, 226, 247, 0.5);
  }
  60% {
    box-shadow: 0 0 15px rgba(15, 226, 247, 0.7);
  }
  80% {
    box-shadow: 0 0 15px rgba(15, 226, 247, 0.9);
  }
  100% {
    box-shadow: 0 0 15px white;
  }
}
.pdf-icon.green-icon {
  animation: glowing-green-animation 2.5s; /* Set animation duration to 2 seconds */
  transition: filter 3s ease-in-out; /* Add a transition for smooth color change */
}

@keyframes glowing-green-animation {
  0% {
    filter: invert(100%)
  }
  50% {
    filter:  invert(0%); /* Rotate color halfway */
  }
  70% {
    filter: invert(60%) sepia(2000%) saturate(1000%) hue-rotate(20deg) drop-shadow(1px 1px 0 green);
  }
  80% {
    filter: invert(80%) sepia(2000%) saturate(1000%) hue-rotate(20deg) drop-shadow(1px 1px 0 green);
  }
  100% {
    filter: invert(100%) sepia(2000%) saturate(1000%) hue-rotate(20deg) drop-shadow(1px 1px 0 green) brightness(100%);
  }
}

.animate-remove {
  animation: colorChange 2s; /* Apply the same color change animation */
  transition: filter 3s ease-in-out; /* Add a transition for smooth color change */
}

</style>
