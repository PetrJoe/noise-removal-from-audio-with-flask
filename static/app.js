$(document).ready(function() {
    $('#fileUploadForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submit action

        var formData = new FormData();
        var audioFile = $('#audioFile')[0].files[0]; // Get the file from the input
        if (!audioFile) {
            alert('Please select a file first.');
            return;
        }
        formData.append('audio_file', audioFile);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false, // Tell jQuery not to process the data
            contentType: false, // Tell jQuery not to set contentType
            beforeSend: function() {
                $('#loadingMessage').removeClass('hidden'); // Show loading message before sending data
            },
            success: function(data) {
                console.log(data);
                if (data.processed_file) {
                    var downloadLinkHTML = '<a href="/download/' + data.processed_file + '" target="_blank">Download Processed File</a>';
                    $('#downloadLink').html(downloadLinkHTML);
                }
                alert(data.message || 'File processed successfully');
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                alert('Error processing file');
            },
            complete: function() {
                $('#loadingMessage').addClass('hidden'); // Hide loading message once the request is complete
            }
        });
    });
});
