function downloadRun() {
    const element = document.getElementById('run-content');
    const button = document.querySelector("button");
    button.style.display = "none";
    const options = {
        margin: 0.5,
        filename: 'Mortal_Trials_Run.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().set(options).from(element).save().then(() => {
        button.style.display = "block";
    });
}