let currentStep = 1;
const totalSteps = 4;

function updateStepDisplay() {
  for (let i = 1; i <= totalSteps; i++) {
    document.getElementById(`step-${i}`).classList.add("hidden");
  }
  document.getElementById(`step-${currentStep}`).classList.remove("hidden");
  document.getElementById("progress").innerText = `Étape ${currentStep} sur ${totalSteps}`;
}

function nextStep() {
  if (currentStep < totalSteps) {
    currentStep++;
    updateStepDisplay();
  }
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    updateStepDisplay();
  }
}

// Initialiser à l’ouverture de la page
document.addEventListener("DOMContentLoaded", updateStepDisplay);
