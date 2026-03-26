import type { MockConfig } from "../types";
import jwt from 'jsonwebtoken';

const generateToken = () => {
    const payload = {
        username: "test",
        exp: Math.floor((Date.now() + 30 * 60 * 1000) / 1000), // 30 minutes from now
    };

    // Clé secrète pour les tests
    const SECRET_KEY = 'cle-secrette-pour-les-tests';

    return jwt.sign(payload, SECRET_KEY);
};

export const loginMocks = {
    notFound: {
        url: '*/**/user/login',
        response: {
            status: 404,
            json: { message: "User not found" }
        }
    },
    success: {
        url: '*/**/user/login',
        response: {
            status: 200,
            json: {
                "token": generateToken()
            }
        }
    }
} satisfies Record<string, MockConfig>;