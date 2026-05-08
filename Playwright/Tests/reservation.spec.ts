import { test, expect, type Page } from '@playwright/test';
import { ApiMocker }    from '../Helper/mockApi';
import { MOCK_EVENT, VALID_FORM, MOCK_BOOK_SUCCESS } from '../Helper/Mocks/reservation.mock';

async function fillFormOnly(page: Page, data = VALID_FORM) {
  await page.locator('[name="clientFname"]').fill(data.clientFname);
  await page.locator('[name="clientLname"]').fill(data.clientLname);
  await page.locator('[name="clientEmail"]').fill(data.clientEmail);
  await page.locator('[name="clientPhone"]').fill(data.clientPhone);
  await page.locator('[name="item"]').fill(data.item);
  await page.locator('[name="itemDescription"]').fill(data.itemDescription);
}

async function acceptWaiver(page: Page) {
  await page.getByTestId('liability-checkbox').focus();
  await page.getByTestId('liability-checkbox').check();
}

async function fillForm(page: Page, data = VALID_FORM) {
  await fillFormOnly(page, data);
  await acceptWaiver(page);
}

async function selectFirstSlot(page: Page) {
  await page.locator('.slot').first().click();
}

test.describe('Gestion des Réservations', () => {

  test.beforeEach(async ({ page }) => {
      await page.clock.install({ time: new Date('2026-07-16T07:55:00') });

      // DEBUG — à enlever après
      page.on('request', req => console.log('REQUEST:', req.method(), req.url()));
      page.on('response', res => console.log('RESPONSE:', res.status(), res.url()));

      const apiMocker = new ApiMocker(page);
      await apiMocker.addMocks([
          { url: "/api/events/active",    method: "GET", response: { status: 200, json: [MOCK_EVENT] } },
          { url: "/api/availableSlots/1", method: "GET", response: { status: 200, json: MOCK_EVENT.slots } },
          { url: "/api/me",               method: "GET", response: { status: 200, json: {} } },
      ]).apply();

      await page.goto('/');
      await expect(page.getByText(/8\s?h\s?00/)).toBeVisible();
  });


  test('affiche les créneaux de l\'événement actif', async ({ page }) => {
    await expect(page.getByText(/8\s?h\s?00/)).toBeVisible();
    await expect(page.getByText(/8\s?h\s?30/)).toBeVisible();
    await expect(page.locator('.slot')).toHaveCount(2);
  });

  test('affiche le nom et la date de l\'événement', async ({ page }) => {
    await expect(page.locator('.event-badge')).toContainText('Atelier Réparation');
    await expect(page.locator('.event-badge')).toContainText('2026');
  });

  test('affiche les 3 sections du formulaire', async ({ page }) => {
    await expect(page.locator('.section-head h2').nth(0)).toContainText('1 —');
    await expect(page.locator('.section-head h2').nth(1)).toContainText('2 —');
    await expect(page.locator('.section-head h2').nth(2)).toContainText('3 —');
  });


  test('sélectionner un créneau coche le radio button', async ({ page }) => {
    const firstSlot = page.locator('.slot').first();
    await firstSlot.click();

    const radio = firstSlot.locator('input[type="radio"]');
    await expect(radio).toBeChecked();
  });

  test('le label du créneau sélectionné a la classe selected', async ({ page }) => {
    const firstSlot = page.locator('.slot').first();
    await firstSlot.click();
    await expect(firstSlot).toHaveClass(/selected/);
  });

  test('changer de créneau désélectionne le précédent', async ({ page }) => {
    const slots = page.locator('.slot');
    await slots.nth(0).click();
    await slots.nth(1).click();

    await expect(slots.nth(0)).not.toHaveClass(/selected/);
    await expect(slots.nth(1)).toHaveClass(/selected/);
  });


  test('bloque la soumission sans créneau sélectionné', async ({ page }) => {
    // fillForm inclut la décharge — seul le créneau manque
    await fillForm(page);
    await page.locator('button.btn-submit').click();

    await expect(page.locator('.alert-error')).toContainText(/plage horaire/i);
    await expect(page.locator('.alert-success')).not.toBeVisible();
  });

  test('bloque la soumission sans décharge cochée', async ({ page }) => {
    await selectFirstSlot(page);
    await fillFormOnly(page);
    await page.locator('button.btn-submit').click();

    await expect(page.locator('.err')).toContainText(/décharge/i);
    await expect(page.locator('.alert-success')).not.toBeVisible();
  });

  test('n\'envoie pas la requête si la validation échoue', async ({ page }) => {
    let requestMade = false;
    await page.route('**/api/book_slot', () => { requestMade = true; });

    await page.locator('button.btn-submit').click();

    await expect(page.locator('.alert-error, .err').first()).toBeVisible();
    expect(requestMade).toBe(false);
  });

  test('doit soumettre une réservation valide', async ({ page }) => {
    await page.route('**/api/book_slot', async (route) => {
      await route.fulfill({ status: 200, json: MOCK_BOOK_SUCCESS });
    });

    await selectFirstSlot(page);
    await fillForm(page);

    const submitBtn = page.locator('button.btn-submit');
    await expect(submitBtn).toBeEnabled();

    const [request] = await Promise.all([
      page.waitForRequest(req =>
        req.url().includes('/api/book_slot') && req.method() === 'POST'
      ),
      submitBtn.click(),
    ]);

    const payload = request.postDataJSON();
    expect(payload.clientFname).toBe('Marie');
    expect(payload.clientLname).toBe('Tremblay');
    expect(payload.clientEmail).toBe('marie@example.com');
    expect(payload.item).toBe('Grille-pain');
    expect(payload.itemDescription).toBe('En panne depuis hier, le bouton de mise en marche est cassé');
    expect(payload.waiverAccepted).toBe(true);
    expect(payload.slot).toBeDefined();
    expect(payload.slot.startAt).toBe('2026-07-16T08:00:00');
    expect(payload.slot.endAt).toBe('2026-07-16T08:15:00');

    await expect(page.getByText(/confirmée/i)).toBeVisible();
    await expect(page.locator('.alert-success')).toContainText('Marie Tremblay');
    await expect(page.locator('.alert-success')).toContainText('marie@example.com');
  });

  test('affiche le nom et courriel dans la confirmation', async ({ page }) => {
    await page.route('**/api/book_slot', async (route) => {
      await route.fulfill({ status: 200, json: MOCK_BOOK_SUCCESS });
    });

    await selectFirstSlot(page);
    await fillForm(page);
    await page.locator('button.btn-submit').click();

    await expect(page.locator('.alert-success')).toContainText('Marie Tremblay');
    await expect(page.locator('.alert-success')).toContainText('marie@example.com');
    await expect(page.locator('button.btn-submit')).not.toBeVisible();
  });


  test('affiche une erreur 400 Django', async ({ page }) => {
    await page.route('**/api/book_slot', async (route) => {
      await route.fulfill({
        status: 400,
        json: { field: "clientEmail", message: "Adresse courriel invalide." },
      });
    });

    await selectFirstSlot(page);
    await fillForm(page);
    await page.locator('button.btn-submit').click();

    await expect(page.locator('.alert-error')).toBeVisible();
    await expect(page.locator('.alert-success')).not.toBeVisible();
  });

  test('affiche une erreur générique en cas d\'erreur réseau', async ({ page }) => {
    await page.route('**/api/book_slot', route => route.abort());

    await selectFirstSlot(page);
    await fillForm(page);
    await page.locator('button.btn-submit').click();

    await expect(page.locator('.alert-error')).toBeVisible();
    await expect(page.locator('.alert-success')).not.toBeVisible();
  });

});