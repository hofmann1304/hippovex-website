// Progressive enhancement: native POST remains available without JavaScript.
const contactForm = document.querySelector('[data-contact-form]');
if (contactForm) {
  const submitButton = contactForm.querySelector('[type="submit"]');
  const statusMessage = contactForm.querySelector('[data-form-status]');
  const english = document.documentElement.lang === 'en';
  const label = submitButton.textContent;
  let sending = false;

  function showStatus(kind, text) {
    statusMessage.hidden = false;
    statusMessage.dataset.state = kind;
    statusMessage.setAttribute('role', kind === 'error' ? 'alert' : 'status');
    statusMessage.textContent = text;
    statusMessage.focus();
  }

  contactForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending || !contactForm.reportValidity()) return;
    sending = true;
    submitButton.disabled = true;
    submitButton.textContent = english ? 'Sending…' : 'Wird gesendet…';
    contactForm.setAttribute('aria-busy', 'true');
    statusMessage.hidden = true;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { Accept: 'application/json' },
        credentials: 'omit',
        signal: controller.signal,
      });
      const result = await response.json();
      if (!response.ok || result.success !== true) throw new Error('Submission not confirmed');
      contactForm.reset();
      showStatus('success', english
        ? 'Thank you! Your request has been submitted. We will reply by email. A beta enquiry does not guarantee a test place.'
        : 'Vielen Dank! Deine Anfrage wurde übermittelt. Du erhältst eine Antwort per E-Mail. Eine Beta-Anfrage garantiert noch keinen Testplatz.');
    } catch {
      // Never claim delivery after an ambiguous network result, and never retry automatically.
      showStatus('error', english
        ? 'We could not confirm your submission. Your entries have been kept. Please try again later.'
        : 'Die Übermittlung konnte nicht bestätigt werden. Deine Angaben bleiben erhalten. Bitte versuche es später erneut.');
    } finally {
      clearTimeout(timeout);
      sending = false;
      submitButton.disabled = false;
      submitButton.textContent = label;
      contactForm.removeAttribute('aria-busy');
    }
  });
}
