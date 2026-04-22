import { test, expect } from '@playwright/test';
import { ApiMocker } from '../Helper/mockApi';
import { MOCK_EVENT, EXPECTED_PAYLOAD } from '../Helper/Mocks/reservation.mock';

test.describe('Gestion des Réservations', () => {

  test.beforeEach(async ({ page }) => {
    await page.clock.install({ time: new Date('2026-07-16T07:55:00') });
    
    const apiMocker = new ApiMocker(page);
    await apiMocker.addMocks([
      { url: "/api/events/active/", method: "GET", response: { status: 200, json: MOCK_EVENT } },
      { url: "/api/me", method: "GET", response: { status: 200, json: {} } }
    ]).apply();

    await page.goto('/');
    await expect(page.getByText('8 h 00')).toBeVisible();
  });

  test('doit soumettre une réservation valide', async ({ page }) => {
    await page.route('**/api/book_slot', async (route) => {
      await route.fulfill({ 
        status: 200, 
        json: { slot_id: 99, startAt: "...", clientEmail: "marie@example.com" } 
      });
    });

    const slotBtn = page.getByRole('button', { name: '8 h 00' });
    await slotBtn.click();    
  
    await page.locator('#firstName').fill('Marie');
    await page.locator('#lastName').fill('Tremblay');
    await page.locator('#email').fill('marie@example.com');
    await page.locator('#phone').fill('514-555-0000');
    await page.locator('#item').fill('Grille-pain');
    await page.locator('#itemDescription').fill('Le bouton de mise en marche est cassé');
    await page.getByTestId('waiver-checkbox').focus(); //permet au test de ralentir pour s'assurer que le checkbox est bien visible avant de tenter de le cocher
    await page.getByTestId('waiver-checkbox').check();

  const submitBtn = page.locator('button.btn-submit');
  await expect(submitBtn).toBeEnabled();

  const [request] = await Promise.all([
    page.waitForRequest(req => 
      req.url().includes('/api/book_slot') && req.method() === 'POST'
    ),
    submitBtn.click()
  ]);

  // 6. Vérification
  const payload = request.postDataJSON();
  expect(payload.clientFname).toBe('Marie');
  expect(payload.itemDescription).toBe('Le bouton de mise en marche est cassé');
  
  await expect(page.getByText(/confirmée/i)).toBeVisible();
  });
});