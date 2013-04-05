# Form related code

$ ->

  # apply placeholder text to input elements by looking for .placeholder-containers
  # these elements wrap the input elements and contain a data attribute with the placeholder text
  # we then use the watermark plugin to apply the placeholder text
  $('.placeholder-container').each (i, el) ->
    $el = $(el)
    $el.find(':nth-child(1)').watermark($el.data('placeholder'), {useNative: false})