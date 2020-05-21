$(document).ready(function () {
    });

    $('img[data-enlargable]').addClass('img-enlargable').click(function(){
        var src = $(this).attr('src');
        var modal;
        function removeModal(){ modal.remove(); $('body').off('keyup.modal-close'); }
        modal = $('<div>').css({
            background: 'RGBA(0,0,0,.5) url('+src+') no-repeat center',
            backgroundSize: 'contain',
            width:'100%', height:'100%',
            position:'fixed',
            zIndex:'10000',
            top:'0', left:'0',
            cursor: 'zoom-out'
        }).click(function(){
            removeModal();
        }).appendTo('body');
        //handling ESC
        $('body').on('keyup.modal-close', function(e){
            if(e.key==='Escape'){ removeModal(); }
        });
    });

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function toggle_reject_reason(obj) {
        var selected_action = $(obj).val();
        if(selected_action === 'reject'){
            $('#reject_reason_div').show();
        }
        else{
            $('#reject_reason_div').hide();
            $("#reject_reason").val([]);
        }
    }

    function toggle_field_reject_reason(obj) {
        var selected_action = $(obj).val();
        var field_id = $(obj).attr("id").split('moderable_')[1];
        if(selected_action === 'reject'){
            $('#reject_reason_div_' + field_id).show();
            $('#reject_reason_' + field_id).prop('required',true);
        }
        else{
            $('#reject_reason_div_' + field_id).hide();
            $('#reject_reason_' + field_id).prop('required',false);
            $('#reject_reason_' + field_id).val([]);
        }
    }

    function user_assign(obj) {
        var unique_id = $(obj).data("unique_id");
        var user_assigned = 0;
        if ($(obj).prop("checked") === true) {
            user_assigned = 0;
        } else if ($(obj).prop("checked") === false) {
            user_assigned = 1;
        }
        var data = {
            "unique_id": unique_id,
            "user_assignment": user_assigned
        }
        var jsonString = JSON.stringify(data);
        $.ajax({
            url: "/moderation/user-assign/",
            method: 'POST',
            data: jsonString,
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
                if (data.message) {
                    show_alert(data.message, "success");
                }
                location.reload();
            },
            error: function (xhr, status, error) {
                var data = xhr.responseJSON;
                if (data.message) {
                    show_alert(data.message, "danger");
                }
            },
        });

    }


    function show_alert(message, type){

        var alert_html = '<div class="alert alert-'+ type +' alert-dismissable fade show">'+
            '<button type="button" class="close" ' +
            'data-dismiss="alert" aria-hidden="true">' +
            '&times;' +
            '</button>' +
            message +
            '</div>';
        $('#alert_div').html(alert_html);
        window.setTimeout(function() {
            $(".alert").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
            });
        }, 2000);
    }

    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove();
        });
    }, 2000);

    $("#submit-form").click(function () {
        if( $("#action").val() === 'reject'){
            $("#reject_reason").prop('required',true);
        }
        else {
            $("#reject_reason").prop('required',false);
        }
        if (document.forms['detail-form'].reportValidity()) {
            var form = $(this).closest("form");
            var obj = $("#detail-form").serializeToJSON({});
            document.forms['detail-form'].reportValidity();
            var jsonString = JSON.stringify(obj);
            $.ajax({
                url: form.attr("action"),
                method: 'POST',
                data: jsonString,
                dataType: 'json',
                contentType: 'application/json',
                success: function (data) {
                    if (data.message) {
                        show_alert(data.message, "success");
                    }
                    window.location.href = $("#entity_breadcrumb").attr("href");
                },
                error: function (xhr, status, error) {
                    var data = xhr.responseJSON;
                    if (data.message) {
                        show_alert(data.message, "danger");
                    }
                }
            });
        } else {
            show_alert("Please Correct Error Below.", "warning");
            document.forms['detail-form'].reportValidity();
        }

    });
