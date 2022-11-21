import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, Observable, of, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';

type AnalysisSuccess = { data: any };
type AnalysisError = { detail: string };
type AnalysisResult = AnalysisSuccess | AnalysisError;

@Injectable({
  providedIn: 'root',
})
export class LexzigService {
  constructor(private http: HttpClient) {}

  analyseCode(code: string): Observable<AnalysisResult> {
    return this.http.post<AnalysisResult>(environment.apiUrl, { code }).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status == 0) {
          console.error(err.message);
          return throwError(() => err);
        }
        return of(err.error as AnalysisError);
      })
    );
  }
}
