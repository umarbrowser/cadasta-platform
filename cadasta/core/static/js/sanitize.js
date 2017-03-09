window.Parsley
  .addValidator('sanitize', function (value, requirement) {
    return !value.match(/.*[<>;\\\/\ud83c[\udf00-\udfff]|\ud83d[\udc00-\ude4f]|\ud83d[\ude80-\udeff]].*/);
  }, 2)
  .addMessage('sanitize', gettext('Input can not contain < > ; \\ / or emojis.'));
