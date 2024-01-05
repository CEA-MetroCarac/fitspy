Models
======

.. figure::  _static/models.png
   :align:   center

.. raw:: html

   <br>

The **Models** frame is used to save and replay a full spectra processing as-is.

:code:`Save Selec.` or :code:`Save All` allows saving the spectra processing associated with the selected spectra in the files selection widget, or with all the spectra (resp.).

:code:`Reload` replays exactly the spectra processing related to the imported *.json*.
This implies that all the files defined in the *.json*  are reachable when reloading.

:code:`Load Model` consists of reloading the spectrum model (baseline and peaks definition, ...) but **not the spectrum file itself**, related to the first model saved in the *.json*.

:code:`Apply to Sel.` or :code:`Apply to All` allows applying the loaded model to the spectra selected in the files selection widget, or to all the spectra (resp.).