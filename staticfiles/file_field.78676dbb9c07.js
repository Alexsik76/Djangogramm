imgInput.onchange = () => {
        let [file] = imgInput.files;
        let imgDestination = imgPrev;
        if (file && imgDestination) {
            let fileName = document.querySelector('#with_filename .file-name');
            fileName.textContent = file.name;
            imgDestination.src = URL.createObjectURL(file)
        }
    };