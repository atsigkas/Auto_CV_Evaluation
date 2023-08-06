<template>
    <div class="popup">
      <div class="popup-content">
        <h2>Final Candidate Rating</h2>
        <hr /> <!-- Add a horizontal line to split the rows -->
        <div class="scrollable-list">
          <ul class="results-list"> <!-- Add a class to the <ul> element -->
            <!-- Iterate through the list of results and display them in the popup -->
            <li v-for="result in results" :key="result.id">{{ result.text }}</li>
          </ul>
        </div>
        <div class="buttons-container">
          <button class="extract-button" @click="extractList">Extract List</button>
          <button class="close-button" @click="closePopup">Close</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      results: {
        type: Array,
        required: true,
      },
    },
    methods: {
      closePopup() {
        // Emit a custom event to notify the parent component to close the popup
        this.$emit("close");
      },
      extractList() {
        // Add functionality for the "Extract List" button here
        console.log("Extract List button clicked!");
      },
    },
  };
  </script>
  
  <style>
  /* Style the popup container and content */
  .popup {
  /* Set the width and height to cover almost the entire screen */
  width: 90vw;
  height: 90vh;
  position: fixed;
  top: 5vh; /* Adjust the top and left positions to center the popup */
  left: 5vw;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  /* Set the width to fill the entire width of the popup */
  width: 100%;
  background-color: transparent; /* Make the background transparent */
  padding: 20px;
  border-radius: 10px;
  box-shadow: none; /* Remove the box shadow */
  color: white; /* Set the text color to white */
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 10px;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
}

hr {
  border: none;
  border-top: 1px solid #fff; /* Set the border color to white */
  margin: 10px 0;
  font-weight: bold; /* Make the text bold */
}

/* Style the buttons container */
.buttons-container {
  display: flex;
  justify-content: space-between; /* To push the buttons to the left and right edges */
  margin-top: 20px;
}

/* Style the close button */
.close-button {
  background-color: #333;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  overflow: hidden;
  position: absolute;
  top: 10px;
  right: 10px;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
}

/* Add the glowing effect for the button when hovering */
.close-button::after {
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

.close-button:hover::after {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

/* Add the glowing effect for the button borders when hovering */
.close-button::before {
  content: "";
  position: absolute;
  bottom: 0; /* Adjust the glowing effect position for the lower border */
  right: 0;
  width: 100%;
  height: 100%;
  border: 2px solid rgba(255, 0, 0, 0.8);
  border-radius: 5px;
  opacity: 0;
  animation: glow-border 1.5s linear infinite;
  pointer-events: none; /* Ensure the glowing effect doesn't interfere with the button click */
}

.close-button:hover::before {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

/* Position the extract button to the bottom center */
.extract-button {
  background-color: #333;
  color: white;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  position: relative; /* Add a position property to the button */
  overflow: hidden; /* Hide the glowing effect outside the button */
}

.extract-button::after {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold; /* Make the text bold */
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.5s ease-out;
  pointer-events: none; /* Ensure the glowing effect doesn't interfere with the button click */
}

.extract-button:hover::after {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

.extract-button::before {
  content: "";
  position: absolute;
  bottom: 0; /* Adjust the glowing effect position for the lower border */
  left: 0;
  width: 100%;
  height: 100%;
  border: 2px solid rgba(0, 128, 0, 0.5);
  border-radius: 5px;
  opacity: 0;
  animation: glow-border 1.5s linear infinite;
  pointer-events: none; /* Ensure the glowing effect doesn't interfere with the button click */
}

.extract-button:hover::before {
  opacity: 1; /* Make the glowing effect visible when hovering */
}

/* Define the animation for the glowing effect */
@keyframes glowing-border {
   0% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.3;
  }
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
}

.scrollable-list {
  max-height: 400px; /* Adjust the height as needed */
  overflow-y: auto;
}

.results-list {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: 'Montserrat', sans-serif;
}
  </style>
  