//if running locally append index.html to all links with a trailing /
if(window.location.protocol.indexOf('file') == 0){

    if(window.jQuery){

        $(document).ready(function(){

            $('a').each(function(){

                var linkURL = ($(this).attr('href') || '');

                if((linkURL.length > 0) && (linkURL.slice(-1) == String.fromCharCode(47))){
                    linkURL += 'index.html';

                    $(this).attr('href', linkURL);
                }
            });
        });
    }
}