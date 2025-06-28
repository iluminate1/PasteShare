$(document).ready(function() {
    // Base API URL
    const API_BASE_URL = 'http://localhost:8000'; // Update this with your API URL
    
    // State management
    let authToken = localStorage.getItem('authToken');
    let currentUser = null;
    let currentPasteUrl = null;
    
    // Initialize modals
    const loginModal = new bootstrap.Modal('#login-modal');
    const registerModal = new bootstrap.Modal('#register-modal');
    
    // Initialize UI based on auth state
    updateAuthUI();
    
    // Load initial data
    loadLanguages();
    loadCategories();
    loadRecentPastes();
    
    // Navigation events
    $('#home-link').click(function(e) {
        e.preventDefault();
        showView('home');
        loadRecentPastes();
    });
    
    $('#create-link').click(function(e) {
        e.preventDefault();
        if (!authToken) {
            alert('Please login to create a paste');
            return;
        }
        showView('create');
    });
    
    $('#public-pastes-link').click(function(e) {
        e.preventDefault();
        showView('home');
        loadRecentPastes();
    });
    
    // Auth events
    $('#login-btn').click(function() {
        loginModal.show();
    });
    
    $('#register-btn').click(function() {
        registerModal.show();
    });
    
    $('#logout-btn').click(function() {
        logout();
    });
    
    // Form submissions
    $('#login-form').submit(function(e) {
        e.preventDefault();
        const username = $('#login-username').val();
        const password = $('#login-password').val();
        login(username, password);
    });
    
    $('#register-form').submit(function(e) {
        e.preventDefault();
        const name = $('#register-name').val();
        const email = $('#register-email').val();
        const password = $('#register-password').val();
        register(name, email, password);
    });
    
    $('#paste-form').submit(function(e) {
        e.preventDefault();
        createPaste();
    });
    
    $('#quick-paste-form').submit(function(e) {
        e.preventDefault();
        createQuickPaste();
    });
    
    $('#comment-form').submit(function(e) {
        e.preventDefault();
        addComment();
    });
    
    $('#profile-form').submit(function(e) {
        e.preventDefault();
        updateProfile();
    });
    
    // Profile actions
    $('#edit-profile-btn').click(function() {
        showView('edit-profile');
        loadCurrentUser();
    });
    
    $('#cancel-edit-btn').click(function() {
        showView('profile');
    });
    
    $('#delete-profile-btn').click(function() {
        if (confirm('Are you sure you want to delete your account? This cannot be undone.')) {
            deleteAccount();
        }
    });
    
    // Functions
    function updateAuthUI() {
        if (authToken) {
            $('#auth-buttons').addClass('d-none');
            $('#user-menu').removeClass('d-none');
            loadCurrentUser();
        } else {
            $('#auth-buttons').removeClass('d-none');
            $('#user-menu').addClass('d-none');
            $('#username-display').text('');
        }
    }
    
    function showView(viewName) {
        $('#home-view, #create-view, #paste-view, #profile-view, #edit-profile-view').addClass('d-none');
        $(`#${viewName}-view`).removeClass('d-none');
    }
    
    function apiRequest(method, endpoint, data = null, requiresAuth = false) {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (requiresAuth && authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }
        
        return $.ajax({
            method: method,
            url: `${API_BASE_URL}${endpoint}`,
            headers: headers,
            data: data ? JSON.stringify(data) : null
        });
    }
    
    function login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        $.ajax({
            method: 'POST',
            url: `${API_BASE_URL}/auth/login`,
            data: formData,
            processData: false,
            contentType: false
        }).done(function(response) {
            authToken = response.access_token;
            localStorage.setItem('authToken', authToken);
            loginModal.hide();
            updateAuthUI();
            loadCurrentUser();
            showView('home');
        }).fail(function(jqXHR) {
            alert('Login failed: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
        });
    }
    
    function register(name, email, password) {
        apiRequest('POST', '/auth/register', {
            name: name,
            email: email,
            password: password
        }).done(function() {
            registerModal.hide();
            alert('Registration successful! Please login.');
        }).fail(function(jqXHR) {
            alert('Registration failed: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
        });
    }
    
    function logout() {
        authToken = null;
        localStorage.removeItem('authToken');
        currentUser = null;
        updateAuthUI();
        showView('home');
    }
    
    function loadCurrentUser() {
        if (!authToken) return;
        
        apiRequest('GET', '/users/me', null, true)
            .done(function(user) {
                currentUser = user;
                $('#username-display').text(user.name);
                $('#profile-name').text(user.name);
                $('#profile-email').text(user.email);
                
                // Show profile actions only for the current user
                $('#profile-actions').removeClass('d-none');
            })
            .fail(function() {
                console.error('Failed to load current user');
            });
    }
    
    function loadLanguages() {
        apiRequest('GET', '/language/all')
            .done(function(languages) {
                const $select = $('#paste-language');
                const $quickSelect = $('#quick-language');
                
                $select.empty().append('<option value="">Plain Text</option>');
                $quickSelect.empty().append('<option value="">Plain Text</option>');
                
                languages.forEach(function(language) {
                    $select.append(`<option value="${language.id}">${language.name}</option>`);
                    $quickSelect.append(`<option value="${language.id}">${language.name}</option>`);
                });
            })
            .fail(function() {
                console.error('Failed to load languages');
            });
    }
    
    function loadCategories() {
        apiRequest('GET', '/category/all')
            .done(function(categories) {
                const $select = $('#paste-category');
                
                $select.empty().append('<option value="">No Category</option>');
                
                categories.forEach(function(category) {
                    $select.append(`<option value="${category.id}">${category.name}</option>`);
                });
            })
            .fail(function() {
                console.error('Failed to load categories');
            });
    }
    
    function loadRecentPastes() {
        apiRequest('GET', '/paste/all')
            .done(function(pastes) {
                const $container = $('#recent-pastes');
                $container.empty();
                
                if (pastes.length === 0) {
                    $container.append('<div class="list-group-item">No public pastes found</div>');
                    return;
                }
                
                pastes.forEach(function(paste) {
                    const authorName = paste.user ? paste.user.name : 'Guest';
                    const languageName = paste.language ? paste.language.name : 'Plain Text';
                    
                    $container.append(`
                        <div class="list-group-item paste-item" data-url="${paste.url}">
                            <div class="d-flex justify-content-between">
                                <span class="paste-title">${paste.title || 'Untitled'}</span>
                                <small class="paste-meta">${new Date(paste.created_at).toLocaleString()}</small>
                            </div>
                            <div class="d-flex justify-content-between">
                                <small class="paste-meta">${authorName}</small>
                                <small class="paste-meta">${languageName} • ${paste.views} views</small>
                            </div>
                        </div>
                    `);
                });
                
                $('.paste-item').click(function() {
                    const pasteUrl = $(this).data('url');
                    viewPaste(pasteUrl);
                });
            })
            .fail(function() {
                console.error('Failed to load recent pastes');
            });
    }
    
    function createPaste() {
        if (!authToken) {
            alert('Please login to create a paste');
            return;
        }
        
        const title = $('#paste-title').val();
        const content = $('#paste-content').val();
        const languageId = $('#paste-language').val() || null;
        const categoryId = $('#paste-category').val() || null;
        const isPrivate = $('#paste-private').is(':checked');
        
        apiRequest('POST', '/paste/', {
            title: title,
            content: content,
            language_id: languageId,
            category_id: categoryId,
            is_private: isPrivate
        }, true)
            .done(function(paste) {
                alert('Paste created successfully!');
                viewPaste(paste.url);
            })
            .fail(function(jqXHR) {
                alert('Failed to create paste: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
            });
    }
    
    function createQuickPaste() {
        const title = $('#quick-title').val();
        const content = $('#quick-content').val();
        const languageId = $('#quick-language').val() || null;
        
        const endpoint = authToken ? '/paste/' : '/paste/guest';
        
        apiRequest('POST', endpoint, {
            title: title,
            content: content,
            language_id: languageId,
            is_private: false
        }, authToken ? true : false)
            .done(function(paste) {
                alert('Paste created successfully!');
                $('#quick-paste-form')[0].reset();
                viewPaste(paste.url);
            })
            .fail(function(jqXHR) {
                alert('Failed to create paste: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
            });
    }
    
    function viewPaste(pasteUrl) {
        currentPasteUrl = pasteUrl;
        
        apiRequest('GET', `/paste/${pasteUrl}`)
            .done(function(paste) {
                $('#paste-view-title').text(paste.title || 'Untitled');
                $('#paste-view-content').text(paste.content);
                $('#paste-view-views').text(paste.views);
                $('#paste-view-created').text(new Date(paste.created_at).toLocaleString());
                
                if (paste.user) {
                    $('#paste-view-author').text(paste.user.name);
                } else {
                    $('#paste-view-author').text('Guest');
                }
                
                if (paste.language) {
                    $('#paste-view-language').text(paste.language.name).removeClass('d-none');
                } else {
                    $('#paste-view-language').addClass('d-none');
                }
                
                if (paste.category) {
                    $('#paste-view-category').text(paste.category.name).removeClass('d-none');
                } else {
                    $('#paste-view-category').addClass('d-none');
                }
                
                // Highlight code if language is detected
                if (paste.language && paste.language.code) {
                    $('#paste-view-content').removeClass().addClass(paste.language.code);
                    hljs.highlightElement(document.getElementById('paste-view-content'));
                }
                
                // Load comments
                loadComments(pasteUrl);
                
                // Show comment form only if user is logged in
                if (authToken) {
                    $('#comment-form').removeClass('d-none');
                } else {
                    $('#comment-form').addClass('d-none');
                }
                
                showView('paste');
            })
            .fail(function() {
                alert('Failed to load paste');
            });
    }
    
    function loadComments(pasteUrl) {
        apiRequest('GET', `/paste/comment/${pasteUrl}`)
            .done(function(comments) {
                const $container = $('#comments-container');
                $container.empty();
                
                if (comments.length === 0) {
                    $container.append('<p>No comments yet</p>');
                    return;
                }
                
                comments.forEach(function(comment) {
                    const commentDate = new Date(comment.created_at).toLocaleString();
                    
                    $container.append(`
                        <div class="comment">
                            <div class="comment-author">${comment.user ? comment.user.name : 'Anonymous'}</div>
                            <div class="comment-date">${commentDate}</div>
                            <div class="comment-text">${comment.text}</div>
                        </div>
                    `);
                });
            })
            .fail(function() {
                console.error('Failed to load comments');
            });
    }
    
    function addComment() {
        if (!authToken) {
            alert('Please login to add a comment');
            return;
        }
        
        const text = $('#comment-text').val();
        
        apiRequest('POST', `/paste/comment/${currentPasteUrl}`, {
            text: text
        }, true)
            .done(function() {
                $('#comment-text').val('');
                loadComments(currentPasteUrl);
            })
            .fail(function(jqXHR) {
                alert('Failed to add comment: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
            });
    }
    
    function updateProfile() {
        const name = $('#edit-name').val();
        const email = $('#edit-email').val();
        const password = $('#edit-password').val();
        
        const data = {
            name: name,
            email: email,
            is_active: true
        };
        
        if (password) {
            data.password = password;
        }
        
        apiRequest('PUT', `/users/${currentUser.id}`, data, true)
            .done(function(updatedUser) {
                currentUser = updatedUser;
                $('#username-display').text(updatedUser.name);
                $('#profile-name').text(updatedUser.name);
                $('#profile-email').text(updatedUser.email);
                showView('profile');
                alert('Profile updated successfully!');
            })
            .fail(function(jqXHR) {
                alert('Failed to update profile: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
            });
    }
    
    function deleteAccount() {
        apiRequest('DELETE', `/users/${currentUser.id}`, null, true)
            .done(function() {
                alert('Account deleted successfully');
                logout();
            })
            .fail(function(jqXHR) {
                alert('Failed to delete account: ' + (jqXHR.responseJSON?.detail || 'Unknown error'));
            });
    }
});