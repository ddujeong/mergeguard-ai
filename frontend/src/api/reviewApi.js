import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const analyzePrApi = async (prUrl) => {

    const response = await axios.post(
        `${API_BASE_URL}/api/v1/reviews/analyze`,
        {
            pr_url: prUrl,
        }
    );

    return response.data;
};