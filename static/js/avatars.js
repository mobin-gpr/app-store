let avatar_id;
$('.avatar-box').click(function(e){
    if($('.active-avatar')[0]){
        $('.active-avatar')[0].classList.remove('active-avatar');
    }
    avatar_id = e.target.classList[0].split('-')[1];
    $(`.avatar-box-${avatar_id}`)[0].classList.add('active-avatar');
})

$("button[name=submit]").click(function (e) {
    if(avatar_id){
        $.ajax({
            url: '/ajax/change-avatar/',
            contentType: 'application/json',
            method: "POST",
            dataType: 'json',
            data: JSON.stringify(
                {
                    avatar_id: avatar_id,
                }
            ),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]")[0].value,
            },
            success: function (result) {
                window.location.href = `/profile/${result.username}`;
            },
            error: function (error) {
                const notyf = new Notyf({
                    duration: 5000,
                    dismissible: true,
                    position: {
                      x: 'center',
                      y: 'bottom',
                    },
                }); 
                notyf.error('خطایی رخ داده است، لطفا مجددا تلاش کنید.');
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
        notyf.error('هنوز آواتار جدیدی انتخاب نکردی!');
    }
})