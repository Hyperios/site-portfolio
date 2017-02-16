(function($) {
    $(function() {
        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Function for checked attributes
        $.fn.toggleAttr = function(attribute, value) { 
            if($(this).attr(attribute)){
                $(this).removeAttr(attribute,value);
            }
            else{ 
                $(this).attr(attribute,value);
            }
        };

        // Toggle for filtering choices 
        $(document).on('click', '#checker', function(event) {
                $(this).toggleClass(function() {
                    if ($(this).is('.deactive_checker')) {
                            $(this).removeClass();
                            return 'active_checker';
                        } else {
                            $(this).removeClass();
                            return 'deactive_checker';
                            }
                });
                $(this).children('input').toggleAttr('checked', 'checked');
        event.preventDefault();
        });


        // For radio input paginator
        $(document).on('click', '#radio_cheker_page', function(event) {
                $('#radio_cheker_page_div').children('label').removeClass();
                $('#radio_cheker_page_div').children('label').attr('class', 'deactive_checker');
                $('#radio_cheker_page_div').children('label').children('input').removeAttr('checked', 'checked');
                $(this).attr('class', 'active_checker');
                $(this).children('input').attr('checked', 'checked');
        event.preventDefault();
        });


        // for registration form
        $("#id_username").change(function () {
            var form = $(this).closest("#registration_form");
            $.ajax({
            url: form.attr("validate-user"),
            data: form.serialize(),
            dataType: 'json',
                success: function (data) {
                  if (data.is_taken) {
                    alert(data.error_message);
                  }
                }
            });
        });

        
        // Login button
        $(document).on('click', '#login_in', function(event) {
            $(this).hide();
            $('#messages').hide();
            $('#login_form').removeClass('hide');
        });


        // Login responce for header login field
        $("#username").change(function () {
            var form = $(this).closest("#login_form");
            $.ajax({
                url: form.attr("login-user"),
                data: form.serialize(),
                dataType: 'json',
                success: function (data) {
                    if (data.is_taken) {
                        alert(data.error_message);
                    }
                }
            });
            event.preventDefault();
        });


        // Total price for header cart
        $(document).on('click', '#add_to_cart', function(event) {
            var url = $(this).children('div').attr('url');
            var id = $(this).children('div').attr('product_id');
            var price = $(this).children('div').attr('product_price');
            $.ajax({
                url: url,
                type: 'POST',
                data: { 'price' : price,
                        'id' : id },
                dataType: 'json',
                success: function (data) {
                    if (data) {
                        $('#cart_count').text(data['count']);
                        $('#cart_total_price').text(data['total_price']);
                    }
                }
            });
            event.preventDefault();
        });


        // Filtering request new_page
        $(document).on('click', '#new_page', function(event) {
            var url = $(this).attr('url');
            var value = $(this).attr('value');
            var page = $(this).attr('page');
            var pagekey = $(this).attr('pn');
            $.ajax({
                url: url,
                type: 'POST',
                data: { "filter_dict" : value,
                        "page" : page,
                        "pagekey" : pagekey
                      },
                success: function (data) {
                    $("html").html(data);
                    $('#radio_cheker_page').attr('class', 'deactive_checker');
                    $(this).attr('class', 'active_checker');
                }
            });
            event.preventDefault();
        });


        // This function set total price in cart page, and header plus count of products
        $(document).on('click', '#col_item', function(event) {  
            var url = $(this).attr('urls'); 
            var col = $(this).attr('add_one');
            var ids = $(this).attr('ids');
            $.ajax({
                url: url,
                type: 'POST',
                data: { 'col' : col,
                        'ids' : ids},
                dataType: 'json',
                success: function (data) {
                    if (data) {
                        var opt = data['ids'].toString();
                        var total_id = data['total_item_id'].toString();
                        $(opt).text(data['col']);
                        $(total_id).text(data['total_item_price'])
                        $('#cart_total_item').text(data['cart_total_item']);
                        $('#cart_total_price').text(data['cart_total_price']);
                        $('#cart_count').text(data['cart_total_item']);
                        $('#cart_total_price2').text(data['cart_total_price']);
                    }
                }
            });
            event.preventDefault();
        });
        
        
        // Send POST for remove all products in the cart, and erase header cart
        $(document).on('click', '#remove_price', function(event) { 
            var url = $(this).attr('urls'); 
            $.ajax({
                url: url,
                type: 'POST',
                data: { },
                dataType: 'json',
                success: function (data) {
                    if (data) {
                        $('#cart_total_price').text(0);
                        $('#cart_count').text(0);
                    }
                }
            });
            event.preventDefault();
        });

    });   
})(jQuery);









