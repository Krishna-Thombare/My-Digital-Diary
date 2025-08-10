// Image preview modal
function openPreview(url) {
    const modal = document.getElementById('imagePreviewModal');
    const viewer = document.getElementById('viewerImage');
    viewer.src = url;
    modal.style.display = 'flex';
    modal.onclick = () => {
        modal.style.display = 'none';
        viewer.src = '';
    };
}

// Upload button logic
document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                document.getElementById('uploadForm').submit();
            }
        });
    }
});
