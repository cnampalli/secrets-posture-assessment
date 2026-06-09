import { useAssessment } from '../assessment/store';
import { useToast } from './Toast';

/**
 * Returns a callback that builds the current domain's assessment record and
 * downloads it as `assessment-<domain>.json`. Shared by the header button and
 * the end-of-questionnaire completion affordance so the download logic lives
 * in one place. Toasts only on partial failure (matches prior header behaviour).
 */
export function useExportRecord(): () => Promise<void> {
  const a = useAssessment();
  const toast = useToast();
  return async function doExport() {
    try {
      const { text, skipped } = await a.exportRecord();
      const blob = new Blob([text], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `assessment-${a.domainId}.json`;
      link.click();
      URL.revokeObjectURL(url);
      if (skipped) toast(`${skipped} file(s) couldn't be exported`);
    } catch {
      toast('Export failed — please try again');
    }
  };
}
