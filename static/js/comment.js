let parent_id = 0


    $('.com__reply').click(function (e){
        let trgt = e.target.classList[0]
        if(parent_id == 0){
            let commet_data = trgt.split('-')
            let user = commet_data[0]
            parent_id = Number(commet_data[1])
        
            $('#cancel-reply')[0].classList.remove('d-none');
            $('#comment-editor .message').append(`<p>شما درحال پاسخ به نظر <a href="#${trgt}">${user}</a> هستید.</p>`);
        }else{
            let commet_data = trgt.split('-')
            let user = commet_data[0]
            parent_id = Number(commet_data[1])
        
            $('#comment-editor .message p').html(`شما درحال پاسخ به نظر <a href="#${trgt}">${user}</a> هستید.`)
        }
    })

    $('#cancel-reply').click(function (){
        parent_id = 0;
        $('#comment-editor .message p').remove()
        $('#cancel-reply')[0].classList.add('d-none');
    })

    $("button[name=submit]").click(function (e) {
        e.preventDefault();
        const notyf = new Notyf({
            duration: 5000,
            dismissible: true,
            position: {
              x: 'left',
              y: 'bottom',
            },
        });     
        if($('#comments')[0].value != ''){
            $(this).html('<span class="loader"></span>');
            $.ajax({
                url: '/apps/ajax/comments/',
                contentType: 'application/json',
                method: "POST",
                dataType: 'json',
                data: JSON.stringify(
                    {
                        app_id: $('.view-app')[0].id,
                        parent_id: parent_id,
                        app_comment: $('#comments')[0].value
                    }
                ),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]")[0].value,
                },
                success: function (result) {
                    $('.loader').remove();
                    $('button[name=submit]').text('ارسال')
                    $('#comments')[0].value = ''
                    if(parent_id != 0){
                        $('#comment-editor .message p').remove()
                        $('#cancel-reply')[0].classList.add('d-none');
                    }
                    notyf.success('نظر شما با موفقیت ارسال شد، پس از تایید نمایش داده خواهد شد.');
                    parent_id = 0
                },
                error: function (error) {
                    if(parent_id != 0){
                        $('#comment-editor .message p').remove()
                        $('#cancel-reply')[0].classList.add('d-none');
                    }
                    $("#loading-layer").fadeOut("slow", function () {
                        $(this).remove();
                    });
                    parent_id = 0
                },
            });
        }else{
            const notyf = new Notyf({
                duration: 5000,
                dismissible: true,
                position: {
                  x: 'center',
                  y: 'bottom',
                },
            }); 
            notyf.error('لطفا متن نظر خود را وارد کنید و سپس بر روی دکمه ارسال کلیک.');
        }
    })


    $(".com-likes > a").click(function (e) {
        e.preventDefault();
        $("body").append('<div id="loading-layer" style="display:none;"></div>');
        $("#loading-layer").fadeIn();
        $.ajax({
          url: '/apps/ajax/comments/reactions/',
          contentType : 'application/json',
          method: "POST",
          dataType: 'json',
          data:JSON.stringify(
            {
                comment_id: e.target.classList[0], 
                type: $(this).attr("data-action")}
        
          ),
          headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": $("[name=csrfmiddlewaretoken]")[0].value,
          },
          success: function (result) {
            if(result.like == result.dislike){
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('neg-comm')
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('pos-comm')
            }else if(result.like >= result.dislike){
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('neg-comm')
                $(`#comment-${e.target.classList[0]}`)[0].classList.add('pos-comm')
            }else{
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('pos-comm')
                $(`#comment-${e.target.classList[0]}`)[0].classList.add('neg-comm')
            }
            $(`.${e.target.classList[0]}-com-like-count`).text(result.like)
            $(`.${e.target.classList[0]}-com-dislike-count`).text(result.dislike)
            $("#loading-layer").fadeOut("slow", function () {
              $(this).remove();
            });
          },
          error: function (error) {
            console.log(error)
            $("#loading-layer").fadeOut("slow", function () {
              $(this).remove();
            });
          },
        });
      });


      $("button[name=news-submit]").click(function (e) {
        e.preventDefault();
        const notyf = new Notyf({
            duration: 5000,
            dismissible: true,
            position: {
              x: 'left',
              y: 'bottom',
            },
        });     
        if($('#comments')[0].value != ''){
            $(this).html('<span class="loader"></span>');
            $.ajax({
                url: '/news/ajax/comments/',
                contentType: 'application/json',
                method: "POST",
                dataType: 'json',
                data: JSON.stringify(
                    {
                        news_id: $('.view-news')[0].id,
                        parent_id: parent_id,
                        news_comment: $('#comments')[0].value
                    }
                ),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    "X-CSRFToken": $("[name=csrfmiddlewaretoken]")[0].value,
                },
                success: function (result) {
                    $('.loader').remove();
                    $('button[name=submit]').text('ارسال')
                    $('#comments')[0].value = ''
                    if(parent_id != 0){
                        $('#comment-editor .message p').remove()
                        $('#cancel-reply')[0].classList.add('d-none');
                    }
                    notyf.success('نظر شما با موفقیت ارسال شد، پس از تایید نمایش داده خواهد شد.');
                    parent_id = 0
                },
                error: function (error) {
                    if(parent_id != 0){
                        $('#comment-editor .message p').remove()
                        $('#cancel-reply')[0].classList.add('d-none');
                    }
                    $("#loading-layer").fadeOut("slow", function () {
                        $(this).remove();
                    });
                    parent_id = 0
                },
            });
        }else{
            const notyf = new Notyf({
                duration: 5000,
                dismissible: true,
                position: {
                  x: 'center',
                  y: 'bottom',
                },
            }); 
            notyf.error('لطفا متن نظر خود را وارد کنید و سپس بر روی دکمه ارسال کلیک.');
        }
    })

    $(".news-com-likes > a").click(function (e) {
        e.preventDefault();
        $("body").append('<div id="loading-layer" style="display:none;"></div>');
        $("#loading-layer").fadeIn();
        $.ajax({
          url: '/news/ajax/comments/reactions/',
          contentType : 'application/json',
          method: "POST",
          dataType: 'json',
          data:JSON.stringify(
            {
                comment_id: e.target.classList[0], 
                type: $(this).attr("data-action")
            }
        
          ),
          headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": $("[name=csrfmiddlewaretoken]")[0].value,
          },
          success: function (result) {
            if(result.like == result.dislike){
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('neg-comm')
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('pos-comm')
            }else if(result.like >= result.dislike){
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('neg-comm')
                $(`#comment-${e.target.classList[0]}`)[0].classList.add('pos-comm')
            }else{
                $(`#comment-${e.target.classList[0]}`)[0].classList.remove('pos-comm')
                $(`#comment-${e.target.classList[0]}`)[0].classList.add('neg-comm')
            }
            $(`.${e.target.classList[0]}-com-like-count`).text(result.like)
            $(`.${e.target.classList[0]}-com-dislike-count`).text(result.dislike)
            $("#loading-layer").fadeOut("slow", function () {
              $(this).remove();
            });
          },
          error: function (error) {
            console.log(error)
            $("#loading-layer").fadeOut("slow", function () {
              $(this).remove();
            });
          },
        });
      });