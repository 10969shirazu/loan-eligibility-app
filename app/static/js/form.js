let currentStep = 1;
const totalSteps = 8;

function showStep(step) {
  document.querySelectorAll('.step').forEach((el, index) => {
    el.classList.toggle('hidden', index !== step - 1);
  });
  document.getElementById('progress').textContent = `Étape ${step} sur ${totalSteps}`;
}

function nextStep() {
  if (currentStep < totalSteps) {
    currentStep++;
    showStep(currentStep);
  }
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('stepForm')) {
    showStep(currentStep);
  }
});
