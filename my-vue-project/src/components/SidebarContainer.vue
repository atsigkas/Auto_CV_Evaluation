<template>
  <div class="sidebar-container">
    <div class="sidebar">
      <h3>Uploaded PDF Files</h3>
      <div class="files-container">
        <ul class="uploaded-files-list">
          <li v-for="(file, index) in localPdfFiles" :key="index" class="file-list-item">
            <span>{{ file.name }}</span>
            <button
              @click="showWarning(index)"
              class="remove-button"
              :class="{ glowing: showConfirmation && removeIndex === index }"
            >
              X
            </button>
          </li>
        </ul>
      </div>
    </div>
    <div v-if="showConfirmation" class="confirmation-message">
      <p>Are you sure you want to remove this file?</p>
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
export default {
  props: {
    pdfFiles: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      localPdfFiles: [...this.pdfFiles],
      showConfirmation: false, // Track whether the confirmation message should be displayed
      dontShowAgain: false, // Track the "Don't show this message again" checkbox
      removeIndex: null, // Index of the file to be removed
    };
  },
  created() {
  // Set dontShowAgain to false when the component is created
  this.dontShowAgain = false;
  this.showConfirmation = false; // Ensure that showConfirmation is set to false
  // Check if there is a value in localStorage and update dontShowAgain accordingly
  console.log('dontShowAgain:', this.dontShowAgain);
  },
  methods: {
    removeFile(index) {
      this.localPdfFiles.splice(index, 1); // Remove the file from the local copy
      this.updatePdfFiles();
    },

    // Method to update the localPdfFiles array
    updateLocalPdfFiles(pdfFiles) {
      this.localPdfFiles = pdfFiles;
      this.updatePdfFiles();
    },
    showWarning(index) {
      if (this.dontShowAgain) {
        this.confirmRemove(index);
      } else {
        this.showConfirmation = true; // Always set showConfirmation to true
        this.removeIndex = index;
      }
    },
    updateLocalStorage() {
      localStorage.setItem('dontShowAgain', this.dontShowAgain.toString());
      console.log('localStorage updated:', this.dontShowAgain);

      if (this.dontShowAgain) {
        this.$emit('update-pdf-files', this.localPdfFiles);
        this.showConfirmation = false; // Hide the confirmation message
      }
    },
    confirmRemove() {
      this.localPdfFiles.splice(this.removeIndex, 1);
      this.updatePdfFiles();

      if (!this.dontShowAgain) {
        this.$emit('update-pdf-files', this.localPdfFiles);
      }

      this.showConfirmation = false;
      this.removeIndex = null;

      localStorage.setItem('dontShowAgain', this.dontShowAgain);
      console.log('confirmRemove - dontShowAgain:', this.dontShowAgain);
    },
    updatePdfFiles() {
      this.$emit('update-pdf-files', this.localPdfFiles);
    },
    cancelRemove() {
      this.showConfirmation = false;
      this.removeIndex = null;
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
  width: 410px; /* Adjust the width to make the sidebar wider */
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center; /* Align items horizontally to the center */
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
  transition: left 0.3s ease-in-out; /* Add the transition back */
}

.sidebar.active {
  left: 0; /* Adjust the left position to fully display the sidebar */
}

.sidebar h3 {
  font-size: 18px;
  color: rgba(234, 182, 118, 0.8);
  margin-bottom: 10px;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
}

.files-container {
  flex: 1;
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
  margin-bottom: 15px;
  padding: 10px; /* Add padding for better readability */
  border-bottom: 1px solid rgba(15, 226, 247, 0.6); /* Add a border between list items */
  text-align: right; /* Align the text to the center */
}

.uploaded-files-list li:last-child {
  border-bottom: none; /* Remove border for the last list item */
}

/* Apply word wrapping to the list items */
.uploaded-files-list li {
  word-wrap: break-word;
  white-space: normal;
}

.file-list-item {
  color: white;
  margin-bottom: 5px;
  padding: 5px; /* Add padding for better readability */
  border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* Add a border between list items */
  text-align: center; /* Align the text to the center */
  /* Apply word wrapping to the list items */
  word-wrap: break-word;
  white-space: normal;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
  /* Avoid text from being cut off at the right */
  overflow: hidden;
}

.remove-button {
  background-color: rgba(234, 182, 118, 0.8);
  color: white;
  border: none;
  padding: 3px 6px;
  border-radius: 80%;
  cursor: pointer;
  font-size: 15px;
  margin-left: 10px;
}

.confirmation-message {
  position: fixed;
  top: 10%; /* Vertically center the confirmation box */
  left: calc(410px + 40px); /* Position it next to the sidebar */
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
  animation: glowing-animation 1.5s infinite alternate;
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
    box-shadow: 0 0 15px rgba(15, 226, 247, 1);
  }
}
</style>
