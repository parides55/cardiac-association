/*
 * Bulk upload for gallery albums in the Django admin.
 *
 * Files go from the browser straight to Cloudinary (no request passes through
 * our own server, so there is no 30 second timeout and no size limit of ours).
 * When the queue is finished, the list of uploaded files is sent to Django,
 * which creates the GalleryImage / GalleryVideo rows.
 */
(function () {
    'use strict';

    const configElement = document.getElementById('bulk-upload-config');
    const button = document.getElementById('bulk-upload-button');
    const statusElement = document.getElementById('bulk-upload-status');
    if (!configElement || !button) {
        return;
    }
    const config = JSON.parse(configElement.textContent);

    function setStatus(message, isError) {
        statusElement.textContent = message;
        statusElement.style.color = isError ? '#ba2121' : '';
    }

    function csrfToken() {
        const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return input ? input.value : '';
    }

    function postJson(url, payload) {
        return fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken()},
            body: JSON.stringify(payload),
        }).then(function (response) {
            if (!response.ok) {
                throw new Error('Request failed (' + response.status + ')');
            }
            return response.json();
        });
    }

    if (!window.cloudinary || !window.cloudinary.createUploadWidget) {
        button.disabled = true;
        setStatus('The upload tool could not be loaded. Check your internet connection and reload the page.', true);
        return;
    }

    let uploaded = [];
    let saving = false;

    function saveUploaded() {
        if (saving || uploaded.length === 0) {
            return;
        }
        saving = true;
        const items = uploaded;
        uploaded = [];
        setStatus('Saving ' + items.length + ' file(s) to the album…');
        postJson(config.saveUrl, {items: items})
            .then(function (result) {
                let message = 'Added ' + result.images + ' photo(s) and ' + result.videos + ' video(s).';
                if (result.skipped) {
                    message += ' ' + result.skipped + ' file(s) could not be added.';
                }
                setStatus(message + ' Reloading…');
                window.location.reload();
            })
            .catch(function (error) {
                // Keep the list so that pressing the button again retries the save.
                uploaded = items.concat(uploaded);
                saving = false;
                setStatus('The files were uploaded but could not be saved to the album (' +
                    error.message + '). Close this message and press the upload button to retry.', true);
            });
    }

    const widget = window.cloudinary.createUploadWidget({
        cloudName: config.cloudName,
        apiKey: config.apiKey,
        folder: config.folder,
        uploadSignature: function (callback, paramsToSign) {
            postJson(config.signUrl, {params_to_sign: paramsToSign})
                .then(function (result) { callback(result.signature); })
                .catch(function (error) {
                    setStatus('Could not start the upload (' + error.message + ').', true);
                });
        },
        sources: ['local', 'url', 'camera'],
        multiple: true,
        maxFiles: 200,
        resourceType: 'auto',
        clientAllowedFormats: ['image', 'video'],
        showUploadMoreButton: true,
    }, function (error, result) {
        if (error) {
            setStatus('Upload error: ' + (error.statusText || error.message || 'unknown error'), true);
            return;
        }
        if (!result) {
            return;
        }
        if (result.event === 'success') {
            const info = result.info;
            uploaded.push({
                public_id: info.public_id,
                version: info.version,
                signature: info.signature,
                resource_type: info.resource_type,
                format: info.format,
                original_filename: info.original_filename,
            });
            setStatus(uploaded.length + ' file(s) uploaded…');
        } else if (result.event === 'queues-end' || result.event === 'close') {
            saveUploaded();
        }
    });

    button.addEventListener('click', function () {
        if (uploaded.length > 0) {
            saveUploaded();  // retry a save that failed earlier
        } else {
            widget.open();
        }
    });

    // Don't lose finished uploads if the page is closed before they are saved.
    window.addEventListener('beforeunload', function (event) {
        if (uploaded.length > 0 && !saving) {
            event.preventDefault();
            event.returnValue = '';
        }
    });
})();
